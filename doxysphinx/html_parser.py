# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""
The html_parser module contains the html parser that will load and process the html files.

To allow several :mod:`writer` implementations to pick up and handle the result of that parsing a html parser
in a neutral way the parser will change all relevant rst/sphinx markup elements to `<snippet>`-elements.
"""

import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from textwrap import dedent
from typing import List, Optional, Protocol, Set

from lxml import html as etree  # nosec: B410
from lxml.etree import _Element, _ElementTree  # nosec: B410


@dataclass
class HtmlParseResult:
    """Capsules a parsed and processed html tree with meta information."""

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
    used_snippet_formats: Optional[Set[str]]
    """The list of snippet format that are used inside the html tree if any.
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


class ElementProcessor(Protocol):
    """An ElementProcessor processes specific html elements, one at a time.

    Typically this is used to either clean up or transform the elements into a neutralized format.
    """

    elements: List[str] = []
    """A list of html element names this processor can process.

       This is for pre-filtering html elements (an optimization). This processors try_process method
       is only called on these elements.
    """

    is_final: bool = True
    """Whether other processors should be called after this one.

       With a "final processor" (is_final == True) processing of an element stops (no other processors considered)
       once the try_process method returns True.
    """

    format: str = "None"
    """The format this element processor processes... like 'rst', 'md' etc."""

    def try_process(self, element: _Element) -> bool:
        """Try to process an element.

        :param element: The element to check and process
        :return: Whether the "processor did it's thing"/"processing was applied" (True) or not (False)
        """
        return False


class RstInlineProcessor:
    """Element Processor for inline rst elements."""

    elements = ["code"]
    format = "rst"
    is_final = True

    rst_role_regex = re.compile(
        r":(?P<role_name>[A-Za-z0-9-_:]*?):[`'\"](?P<role_content>.*?)[`'\"]", re.MULTILINE | re.DOTALL
    )

    def try_process(self, element: _Element) -> bool:
        """Try to process an rst inline element into a neutralized format.

        :param element: The html element to process
        :return: True if the element was processed else False
        """
        # check for content
        if not element.text:
            return False

        # check if syntax matches sphinx/rst role
        normalized_content = element.text.strip()
        match = self.rst_role_regex.match(normalized_content)
        if match is None:
            return False

        role = match.group("role_name")
        content = match.group("role_content")

        element.tag = "snippet"
        element.text = f":{role}:`{content}`"

        _ensure_newline_before_element(element)
        _ensure_newline_after_element(element)

        element.attrib["type"] = "rst:inline"

        # and here the "secret ingredient" to get inline blocks working:
        # If doxygen renders an outer <p>-tag then inside cannot be other block element tags (by html rules),
        # and sphinx will wrap all blocks with <p>-tags. The browsers will then close opened p tags if they
        # come to a nested block element tag (e.g. a div or another p-tag) which makes our inline css trick
        # obsolete. That's why we change any parent p tag to a div tag here:
        parent = element.getparent()
        if parent is None:
            raise AssertionError("parent is None which cannot happen!? Critical Error!")

        if parent.tag == "p":
            parent.tag = "div"
        parent.attrib["class"] = "doxysphinx-inline-parent"

        return True


class RstBlockProcessor:
    """Element Processor for rst block elements."""

    elements = ["code", "pre"]
    format = "rst"
    is_final = True

    _marker_regex = re.compile(
        r"^("  # begin of the line
        r"{rst}"  # doxysphinx marker
        r"|\.\. [A-Za-z][A-Za-z0-9]+::.*?"  # directive autodetection
        r"|embed:rst(:leading-(asterisk|slashes))?"  # breathe compatibility markers
        r")\s*\r?\n",  # end if the line
        re.MULTILINE,
    )

    def try_process(self, element: _Element) -> bool:
        """Try to process an rst block element into a neutralized format.

        :param element: The html element to process
        :return: True if the element was processed else False
        """
        text = _flattened_element_text(element)
        if not text:
            return False

        if content := _try_parse_rst_block_content(text):

            # add newlines around the element tags to have the beginning and closing tags at the beginning of line each
            _ensure_newline_before_element(element)
            _ensure_newline_after_element(element)

            # add newlines around the content if necessary to have the content in new lines
            content = "\n" + content if not _starts_with_newline(content) else content
            content = content + "\n" if not _ends_with_newline(content) else content

            # process/transform element
            element.clear(keep_tail=True)  # type: ignore
            element.tag = "snippet"
            element.text = content
            element.attrib.clear()
            element.attrib["type"] = "rst:block"
            return True

        return False


class PreToDivProcessor:
    """This Element Processor will change <pre>-tags to <div class="fragments"> tags.

    We do this because doxysphinx will linearize html output in the writer to have it in one line in
    the raw html directive. However this will destroy the newlines in pre tags. To overcome that
    We change the pre output here to a div with inner line divs (which is also supported by doxygen).

    This should be the last processor applied (when everything else is done).
    The reason is that it gets really hard to debug if we change the structure inbetween processors.
    """

    elements = ["pre"]
    format = ""
    is_final = True

    def try_process(self, element: _Element) -> bool:
        """Transform a pre element into a div element.

        :param element: The html element to process
        :return: True if the element was processed else False
        """
        text = _flattened_element_text(element)
        if not text:
            return False

        text = dedent(text)

        # remove first empty lines at the start and at the end if any
        lines = text.split("\n")
        if lines[0].strip() == "":
            lines.pop(0)
        if lines[-1].strip() == "":
            lines.pop()

        element.clear(keep_tail=True)  # type: ignore
        element.tag = "div"
        element.attrib["class"] = "fragment"
        for line in lines:
            line_div = etree.Element("div")
            line_div.attrib["class"] = "line"
            line_div.text = line
            element.append(line_div)

        return True


class MarkdownRstBlockProcessor:
    """Element Processor for doxygen markdown block elements.

    This processor will check if the first line in the markdown block is either a supported marker or
    a directive (auto detection feature).

    Markdown block elements in doxygen are getting rendered different to verbatim content.
    Each Markdown block (delimited with 3 backticks) will be something like this in html:

    .. code-block:: html

       <div class="fragment">
         <div class="line">{rst}</div>
         <div class="line">This is rst content</div>
         <div class="line"> </div>
         <div class="line">anything can be used here...</div>
         <div class="line"> </div>
         <div class="line">like an admonition:</div>
         <div class="line"> </div>
         <div class="line">..admonition::</div>
         <div class="line">  </div>
         <div class="line">  test</div>
       </div>
    """

    elements = ["div"]
    format = "rst"
    is_final = True

    _marker_regex = re.compile(
        r"^("  # begin of the line
        r"{rst}"  # doxysphinx marker
        r"|\.\. [A-Za-z][A-Za-z0-9]+::.*?"  # directive autodetection
        r"|embed:rst(:leading-(asterisk|slashes))?"  # breathe compatibility markers
        r")$",  # end if the line
        re.MULTILINE,
    )

    def try_process(self, element: _Element) -> bool:
        """Try to process an rst block element into a neutralized format.

        :param element: The html element to process
        :return: True if the element was processed else False
        """
        if element.get("class") != "fragment":
            return False

        lines = [_flattened_element_text(e) for e in element if e.tag == "div" and e.get("class") == "line"]

        text = "\n".join(lines)

        if content := _try_parse_rst_block_content(text):

            # add newlines around the element tags to have the beginning and closing tags at the beginning of line each
            _ensure_newline_before_element(element)
            _ensure_newline_after_element(element)

            # add newlines around the content if necessary to have the content in new lines
            content = "\n" + content if not _starts_with_newline(content) else content
            content = content + "\n" if not _ends_with_newline(content) else content

            # process/transform element
            element.clear(keep_tail=True)  # type: ignore
            element.tag = "snippet"
            element.text = content
            element.attrib.clear()
            element.attrib["type"] = "rst:block"
            return True

        return False


def _flattened_element_text(element: _Element) -> str:
    """Flatten (removes children but keeps the text and html nodes) an element text."""
    text = element.text
    if not text:
        return ""

    if len(element) > 0:  # test if element has children
        text = "".join(element.itertext())  # type: ignore

    # old implementation that will render the inner html out (maybe we need this in future?)
    # rendered_html_including_children = etree.tostring(element, encoding="unicode", with_tail=False).strip()
    # tag, tag_end_char, rest = rendered_html_including_children.partition(">")
    # close_tag = f"</{element.tag}>"
    # text = rest[: -len(close_tag)]

    return text


def _starts_with_newline(text: str):
    return text.strip(" \t").startswith("\n")


def _ends_with_newline(text: str):
    return text.strip(" \t").endswith("\n")


def _lstrip_str(to_strip: str, from_text: str) -> str:
    ws_stripped = from_text.lstrip()
    if ws_stripped.startswith(to_strip):
        return ws_stripped[len(to_strip) :]

    # shouldn't happen very often for comments
    return from_text


def _remove_doxygen_comment_prefixes(text: str) -> str:
    stripped = text.lstrip()
    # if leading slashes syntax
    if stripped.startswith("///"):
        lines = [_lstrip_str("///", line) for line in text.split("\n")]
        return "\n".join(lines)
    # if asterisk syntax
    elif stripped.startswith("*"):
        lines = [_lstrip_str("*", line) for line in text.split("\n")]
        return "\n".join(lines)
    # if doubleslash exclamationmark syntax
    elif stripped.startswith("//!"):
        lines = [_lstrip_str("//!", line) for line in text.split("\n")]
        return "\n".join(lines)

    return text


def _try_parse_rst_block_content(text: str) -> Optional[str]:
    if not text:
        return None

    stripped = text.strip()
    first_line, _, all_lines_after = stripped.partition("\n")
    cleaned_line = _remove_doxygen_comment_prefixes(first_line).strip()

    relevant_content = ""
    if cleaned_line in ["{rst}", "embed:rst", "embed:rst:leading-slashes", "embed:rst:leading-asterisk"]:
        relevant_content = all_lines_after
    elif cleaned_line.startswith(".. ") and "::" in cleaned_line:
        relevant_content = text
    else:
        return None

    clean_content = _remove_doxygen_comment_prefixes(relevant_content)
    dedented_content = dedent(clean_content)
    return dedented_content


def _ensure_newline_before_element(element: _Element):
    """Ensure that there is at least one newline character (\\n) before the given element.

    We need this later during the write phase (see :mod:`writer`) which is line oriented.
    When we have a newline in front of our <snippet> elements we can find them more easily/efficiently.
    """
    previous_tag = element.getprevious()
    if previous_tag is not None:
        if previous_tag.tail:
            if not _ends_with_newline(previous_tag.tail):
                previous_tag.tail = f"{previous_tag.tail}\n"
        else:
            previous_tag.tail = "\n"
    else:
        parent_tag = element.getparent()
        if parent_tag is None:
            return
        if parent_tag.text:
            if not _ends_with_newline(parent_tag.text):
                parent_tag.text = f"{parent_tag.text}\n"
        else:
            parent_tag.text = "\n"


def _ensure_newline_after_element(element: _Element):
    """Ensure that there is at least one newline character (\\n) after the given element.

    We need this later during the write phase (see :mod:`writer`) which is line oriented.
    When we have a newline after of our <snippet> elements we can find them more easily/efficiently.
    """
    if not element.tail:
        element.tail = "\n"
        return

    if not _starts_with_newline(element.tail):
        element.tail = f"\n{element.tail}"


class DoxygenHtmlParser:
    """Parser for Doxygen HTML output files."""

    _logger = logging.getLogger(__name__)

    _processors: List[ElementProcessor] = [
        RstInlineProcessor(),
        RstBlockProcessor(),
        MarkdownRstBlockProcessor(),
        PreToDivProcessor(),
    ]

    def __init__(self, source_directory: Path):
        """
        Create an instance of a doxygen html parser.

        :param source_directory:  the directory where the html files are located.
        """
        self._source_directory = source_directory
        # self._parser = etree.HTMLParser(huge_tree=True, recover=False)

    def parse(self, file: Path) -> HtmlParseResult:
        """Parse a doxygen HTML file into an ElementTree and normalize its inner data to contain <rst>-tags.

        :param file: The html file to parse
        :type file: Path
        :return: The result of the parsing
        :rtype: ParseResult
        """
        tree = etree.parse(file.as_posix())  # type: ignore # nosec B320

        meta_title: str = tree.find("//title").text  # type: ignore
        first, *_, last = meta_title.split(":")
        project = first.strip()
        title = last.strip()

        used_snippet_formats = self._normalize_tree_and_get_used_formats(tree)

        return HtmlParseResult(file, project, meta_title, title, used_snippet_formats, tree)

    def _should_parse(self, source: str) -> bool:
        # if no supported element (identified by closing tag) is in the file...
        if not any(f"</{element}>" in source for element in self._all_supported_elements()):
            # fast exit
            return False

        # get content of each element and

        return True

    @staticmethod
    @lru_cache(maxsize=2)
    def _all_supported_elements() -> Set[str]:
        return {e for p in DoxygenHtmlParser._processors for e in p.elements}

    def _normalize_tree_and_get_used_formats(self, tree) -> Set[str]:
        """Normalize a doxygen html tree.

        Searches for pre and code tags, re-formats them and creates different <snippet-*>-tags out of it.
        Will also put a newline behind the closing tag because it's necessary to have lines that can be clearly
        assigned to either html-content or snippet content (and in the un-normalized source html we've got them mixed
        at the closing tag).
        """
        used_snipped_formats = set()

        # prefetch element candidates.
        # We do that because if there are bugs in a processor which will change the tree one might get strange
        # behaviors here (processors not applied because the elements where changed during iteration).
        # So this is just a means to make debugging easier...
        element_candidates = list(tree.iter(*self._all_supported_elements()))

        # search for all supported elements in element tree
        for element in element_candidates:

            # try to apply each processor...
            for processor in self._processors:

                # if the current element isn't supported by the current processor skip to the next one
                if element.tag not in processor.elements:
                    continue

                # try to process the element
                if not self._try_process(element, processor):
                    continue

                # if it was processed add the used format to the output...
                if processor.format:
                    used_snipped_formats.add(processor.format)

                # if the processor is final (no further processors considered) -> break the loop
                if processor.is_final:
                    break

        return used_snipped_formats

    def _try_process(self, element: _Element, processor: ElementProcessor) -> bool:
        # fail if element isn't supported by processor
        if element.tag not in processor.elements:
            return False

        # fail if processing returns
        processed = processor.try_process(element)
        return processed
