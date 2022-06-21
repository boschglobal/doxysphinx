# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""
The html_parser module contains the html parsers that will load the html files.

To allow several :mod:`writer` implementation to pick up and handle the result of that parsing a html parser
must also transform rst snippets into <rst>-nodes.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Protocol, Union

from lxml import etree  # nosec: B410
from lxml.etree import _ElementTree  # nosec: B410


@dataclass
class HtmlParseResult:
    """Capsules a parsed html tree with meta information."""

    html_input_file: Path
    """The html file that was parsed.
    """
    project: str
    """The project where this html file belongs to.
       This can be e.g. a directory name or a component/module name etc.
    """
    meta_title: str
    """The html meta title if present in the original html.
       If not just set to document title
    """
    document_title: str
    """The document title. This is the title that is visible e.g.
       in sphinx menu structure.
    """
    contains_rst: bool
    """Whether the tree contains any rst snippet (this is needed for rst generation
       in a writer)
    """
    tree: _ElementTree
    """The html/xml element tree.
    """


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class HtmlParser(Protocol):
    """Html Parser Protocol for parsing html files into a neutral format (that can be then processed further).

    You own html parser should find/generate all rst-content in <rst>-tags.
    The further tooling can then work with that.
    """

    def __init__(self, source_directory: Path):
        """Create a new instance of this HTML Parser.

        :param source_directory: the parsing source directory (this is maybe necessary
            in some cases for resolvingrelative paths)
        """
        pass

    def parse(self, file: Path) -> HtmlParseResult:
        """Parse a html file.

        This method returns a ParseResult (Tuple[bool, _ElementTree]).
        The first item in the tuple indicates if rst data was found during parsing.
        The second item is the parsed and normalized html as ElementTree.
        It is expected that all rst data in this resulting ElementTree is present in special
        <rst>-tags.

        :param file: The html file to parse
        :return: The result of the parsing
        """
        raise NotImplementedError


class DoxygenHtmlParser:
    """Parser for Doxygen HTML output files."""

    def __init__(self, source_directory: Path):
        """
        Create an instance of a doxygen html parser.

        :param source_directory:  the directory where the html files are located.
        """
        self._source_directory = source_directory
        self._parser = etree.HTMLParser()

    def parse(self, file: Path) -> HtmlParseResult:
        """
        Parse a doxygen HTML file into an ElementTree and normalizes its inner data to contain <rst>-tags.

        :param file: The html file to parse
        :type file: Path
        :return: The result of the parsing
        :rtype: ParseResult
        """
        tree = etree.parse(file.as_posix(), self._parser)  # type: ignore # nosec B320

        meta_title: str = tree.find("//title").text  # type: ignore
        first, *_, last = meta_title.split(":")
        project = first.strip()
        title = last.strip()

        rst_found = self._normalize_tree(tree)

        return HtmlParseResult(file, project, meta_title, title, rst_found, tree)

    def _normalize_tree(self, tree) -> bool:
        """
        Normalize a doxygen html tree.

        Searches for pre and verbatim tags, re-formats them and creates <rst>-tags out of it. Will also put a newline
        behind the closing tag because it's necessary to have lines that can be clearly assigned to either html-content
        or rst content (and in the un-normalized source html we've got them mixed at the closing tag).
        """
        rst_found = False
        for pre_tag in tree.iter("pre", "verbatim"):
            if content := self._parse_content(pre_tag.text):
                pre_tag.tag = "rst"
                pre_tag.text = "\n".join(content) + "\n"

                # add newline after the <rst> tag (so that we can split it up later)
                pre_tag.tail = "\n" if not pre_tag.tail else f"\n{pre_tag.tail}"

                # add newline before the <rst> tag (so that we can split it up later)
                previous_tag = pre_tag.getprevious()
                if previous_tag is not None:
                    if previous_tag.tail:
                        if not previous_tag.tail.endswith("\n"):
                            previous_tag.tail = f"{previous_tag.tail}\n"
                    else:
                        previous_tag.tail = "\n"
                else:
                    parent_tag = pre_tag.getparent()
                    if parent_tag.text:
                        if not parent_tag.text.endswith("\n"):
                            parent_tag.text = f"{parent_tag.text}\n"
                    else:
                        parent_tag.text = "\n"

                pre_tag.attrib.clear()
                rst_found = True
        return rst_found

    def _parse_content(self, text: str) -> Union[List[str], None]:
        """
        Parse the content of @rst directives (=pre/verbatim html nodes) in doxygen comments into a line list.

        If the text contains not the right markers e.g. when using a standard verbatim
        block and no rst block in doxygen comments this method returns None.
        """
        normalized_text = text.strip()

        marker_checks = ((x, normalized_text.startswith(x)) for x in self._supported_markers())

        for marker, found in marker_checks:
            if not found:
                continue

            content = "\n" + normalized_text[len(marker) :]
            # remove doxygen comments
            content = content.replace("\n*", "\n").replace("\n *", "\n")
            content = content.replace("\n///", "\n").replace("\n//!", "\n")

            content_lines = content.split("\n")[1:]

            return content_lines

        return None

    @staticmethod
    def _supported_markers() -> Iterator[str]:
        yield "embed:rst:leading-asterisk"
        yield "embed:rst:leading-slashes"
        yield "embed:rst:inline"
        yield "embed:rst"
