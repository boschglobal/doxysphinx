# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The toc module contains classes related to the toctree generation for doxygen htmls/rsts."""

import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Protocol, Tuple

from doxysphinx.doxygen import read_js_data_file
from doxysphinx.utils.files import write_file
from doxysphinx.utils.iterators import apply


class TocGenerator(Protocol):
    """
    TocGenerator protocol.

    Gets the source_dir (with the html sources) during init and
    each file to possibly generate a toctree directive for in the :meth:`generate_toc_for`
    method. The implementer has then to choose how to implement the toc generation.
    """

    def __init__(self, source_dir: Path):
        """
        Initialize an instance of a TocGenerator.

        :param source_dir: The source directory where all html files reside.
        """

    def generate_toc_for(self, file: Path) -> Iterable[str]:
        """
        Generate a toctree directive for a given file.

        :param file: the file to generate the toctree directive for
        :return: a string interable representing the lines forming the toctree directive
        """
        return []


@dataclass
class _MenuEntry:
    title: str
    docname: str
    url: str
    children: List["_MenuEntry"]
    is_structural_dummy: bool = (
        False  # indicated whether a menu entry references a children's file as a structural dummy
    )
    is_leaf: bool = field(init=False)

    def __post_init__(self):
        if not self.children:
            self.is_leaf = True
        else:
            self.is_leaf = False

    @staticmethod
    def from_json_node(json_node: Dict[str, Any]) -> "_MenuEntry":
        """Create a _MenuEntry from a json node (in doxygen's menudata.js).

        Note that this method will build up a _MenuEntry-tree automatically/recursively

        :param json_node: The json node to generate a _MenuEntry from
        :return: A _MenuEntry representation of the json_node and its' children
        """
        title = json_node["text"]
        url = json_node["url"]
        file = _MenuEntry._docname_from_url(url)
        children = _MenuEntry._get_sphinx_toc_compatible_children(json_node)
        is_structural_dummy = "is_structural_dummy" in json_node and json_node["is_structural_dummy"]
        return _MenuEntry(title, file, url, children, is_structural_dummy)

    @staticmethod
    def _docname_from_url(url: str) -> str:
        return url.split("#")[0].replace(".html", "")

    @staticmethod
    def _get_sphinx_toc_compatible_children(json_node: Dict[str, Any]) -> List["_MenuEntry"]:
        """Get a "sphinx compatible" view of the children.

        We therefore need a special handling for index anchors
        with doxygen we sometimes have urls in menu entries like:
        # - title: url
          - a: globals_enum.html#index_a
          - c: globals_enum.html#index_c
          - e: globals_enum.html#index_e
          - f: globals_enum.html#index_f
            ...
        The problem here is that the sphinx toctree simple cannot handle anchors... so we cannot add these
        links for entries in the parent's toctree. We therefore need to
        - eliminate all childrens with the same name/file down to one last child
        - then check if the parent has the same name/file and in that case get rid of the child completely
        """
        # get all children
        children = [_MenuEntry.from_json_node(c) for c in json_node["children"]] if "children" in json_node else []
        if not children:
            return []

        # get unique (considering .file value) children
        unique_children = []
        current_docname = _MenuEntry._docname_from_url(json_node["url"])
        unique_files = set()

        for child in children:
            if child.docname in unique_files and child.is_leaf:
                continue

            if child.docname == current_docname:
                json_node["is_structural_dummy"] = True

            unique_children.append(child)
            unique_files.add(child.docname)

        # if there is only one child item left and if that's the same as the current item - get rid of it
        current_docname = _MenuEntry._docname_from_url(json_node["url"])
        if len(unique_children) == 1 and unique_children[0].docname == current_docname and unique_children[0].is_leaf:
            json_node["is_structural_dummy"] = False
            return []

        return unique_children


class DoxygenTocGenerator:
    """
    A TocGenerator for doxygen.

    Will read the menudata.js to check whether a toctree
    directive needs to be generated or not.
    """

    def __init__(self, source_dir: Path):
        """
        Initialize an instance of a TocGenerator.

        :param source_dir: The source directory where the doxygen html files reside.
        """
        self._source_dir = source_dir

        self._menu: _MenuEntry = self._load_menu_tree(source_dir / "menudata.js")

        # self._project_name, self._project_number = self._parse_project_infos()
        self._doxy_html_template: Tuple[str, str] = self._parse_template()

        # create rst files for those structural dummies doxygen is using...
        structural_dummies = [e for e in self._flatten_tree(self._menu) if e.is_structural_dummy]
        apply(structural_dummies, self._prepare_structural_dummy)
        apply(structural_dummies, self._create_toc_file_for_structural_dummy)

        self._menu_lookup: Dict[str, _MenuEntry] = dict(
            {e.docname: e for e in self._flatten_tree(self._menu) if not e.is_leaf}
        )

    def _parse_template(self) -> Tuple[str, str]:
        """Parse a "doxygen html template shell" out of the index.html file.

        :return: A Tuple containing the doxygen html before the content area and the content after the content area.
        """
        # load html file as string and remove the newline chars
        blueprint = self._source_dir / "index.html"
        complete_html = blueprint.read_text()
        linearized_html = complete_html.replace("\n", "").replace("\r", "")

        # split the html string on the content element
        # (so that we can use the 2 parts and inject our content in the middle)
        split_start_search = r"<!--header--><div class=\"contents\">"
        split_end_search = r"</div><!-- contents -->"
        split_regex = re.compile(f"{split_start_search}.*?{split_end_search}")
        splitted = split_regex.split(linearized_html)
        if len(splitted) != 2:
            raise Exception(
                "couldn't parse html template for toc dummies from index.html. "
                "Maybe the format of doxygen has changed? Or do you have a custom template? In that case: "
                "we search for the following regex to find anything except the content: "
                '<!--header--><div class="contents">.*</div><!-- contents -->'
            )
        prefix, suffix = splitted

        # replace the original index title with a marker that we can easily replace afterwards
        replace_regex = re.compile('(?<=<div class="title">).*?(?=</div>)')
        prefix_replaced = replace_regex.sub("@@@-TITLE-@@@", prefix)

        return prefix_replaced + split_start_search.replace('\\"', '"'), split_end_search + suffix

    def _prepare_structural_dummy(self, structural_dummy: _MenuEntry):
        clean_title = structural_dummy.title.replace(" ", "_").lower()
        toc_docname = f"{structural_dummy.docname}_{clean_title}"
        structural_dummy.docname = toc_docname

    def _create_toc_file_for_structural_dummy(self, structural_dummy: _MenuEntry):

        prefix, suffix = self._doxy_html_template

        content = [
            f".. title:: {structural_dummy.title}",
            "",
            f"{structural_dummy.title}",
            f"{'-' * len(structural_dummy.title)}",
            "",
            ".. container:: doxygen-content",
            "",
            "   .. raw:: html",
            "",
            "      " + prefix.replace("@@@-TITLE-@@@", structural_dummy.title),
            "",
            "   .. toctree::",
            "      :maxdepth: 4",
            "",
            *[f"      {item.title} <{item.docname}>" for item in structural_dummy.children],
            "",
            "   .. raw:: html",
            "",
            "      " + suffix,
            "",
        ]

        file = self._source_dir / f"{structural_dummy.docname}.rst"

        write_file(file, content)

    def _load_menu_tree(self, menu_data_js_path: Path) -> _MenuEntry:
        menu = read_js_data_file(menu_data_js_path)
        items = menu["children"]

        children = [_MenuEntry.from_json_node(c) for c in items]
        root, *_ = children
        _, *children_without_root = children
        root_copy = replace(root, children=children_without_root)
        return root_copy

    def _flatten_tree(self, *entries: _MenuEntry) -> Iterator[_MenuEntry]:
        for entry in entries:
            yield entry
            if not entry.is_leaf:
                yield from self._flatten_tree(*entry.children)

    def generate_toc_for(self, file: Path) -> Iterator[str]:
        """
        Generate a toctree directive for a given file.

        Note that the toctree will only be generated when the file is part of a menu
        structure.
        :param file: the file to generate the toctree directive for
        :return: a string iterator representing the lines forming the toctree directive
        """
        name = file.stem
        if name in self._menu_lookup:
            matching_menu_entry = self._menu_lookup[name]

            children = matching_menu_entry.children
            if not children:  # when the children list is empty no tocs need to be generated.
                return

            yield ".. toctree::"
            yield f"   :caption: {matching_menu_entry.title}"
            yield "   :maxdepth: 2"
            yield "   :hidden:"
            yield ""
            yield from [f"   {item.title} <{item.docname}>" for item in matching_menu_entry.children]
            yield ""
