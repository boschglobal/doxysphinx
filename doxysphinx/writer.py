# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
#  - Aniket Salve, Robert Bosch GmbH
# =====================================================================================
"""The writer module contains classes that write the docs-as-code output files."""
import html
import logging
import re
from itertools import chain
from pathlib import Path
from textwrap import dedent
from typing import Iterator, List, Protocol, Type, Union

from lxml import etree  # nosec: B410, pylint: disable=import-error
from lxml.etree import _ElementTree  # nosec: B410, pylint: disable=import-error

from doxysphinx.html_parser import HtmlParseResult
from doxysphinx.toc import DoxygenTocGenerator, TocGenerator
from doxysphinx.utils.files import write_file

# pylint: disable=logging-fstring-interpolation


class Writer(Protocol):
    """Protocol representing a Writer that write docs-as-code files."""

    def __init__(self, source_directory: Path, toc_generator_type: Type[TocGenerator] = DoxygenTocGenerator):
        """
        Writer constructor protocol.

        :param source_directory: The processing source directory (with the html files).
            Sometimes it's necessary to amend the generated rsts/output files with
            additional data from source directory (typically e.g. to generate a toc).
            For this reason the source directory is an input here
        :param toc_generator_type: the type to use for generating the toc (has to adhere
            the :class:`TocGenerator` protocol.
        """

    def write(self, parse_result: HtmlParseResult, target_file: Path, html_hash: str) -> Path:
        """
        Write a parsed html result to a target file.

        The format of that file is controlled by the concreate Writer implementation.

        :param parse_result: The result of a previous html parser run
        :param target_file: The target file to write
        :return: The written file (should be always identical to target_file input, but
            allows chaining...)
        """
        return Path()


class RstWriter:
    """Writes sphinx-rst files to disk."""

    _logger = logging.getLogger(__name__)

    # compiled regex for combining adjacent rst blocks
    _rst_join_regex = re.compile(r"</snippet>\s*<snippet.*?>")

    # regex for searching inline elements
    _rst_element_regex = re.compile(r"<snippet type=\"(?P<type>.*?)\">((?P<inline_content>.*?)</snippet>)?$")

    def __init__(self, source_directory: Path, toc_generator_type: Type[TocGenerator] = DoxygenTocGenerator):
        """
        Create a new rst writer.

        :param source_directory: Source directory of html files.
        :param toc_generator_type: The toc generator to use.
        """
        self._toc_gen = toc_generator_type(source_directory)

        # cached translation map for safe encoding rst text
        self._rst_safe_encode_map = str.maketrans(
            {
                "_": r"\_",
                "\\": r"\\",
                "^": r"\^",
                "$": r"\$",
                "*": r"\*",
                "`": r"\`",
            }
        )

    def _rst_safe_encode(self, text: str) -> str:
        return text.translate(self._rst_safe_encode_map)

    def write(self, parse_result: HtmlParseResult, target_file: Path, html_hash: str) -> Path:
        """
        Write html content to the target_file.

        :param parse_result: The result of the html parsing (=content + metadata)
        :param target_file:  The target docs-as-code (e.g. rst) file
        :return: The path the file was written to.
        """
        tree = parse_result.tree
        meta_title = parse_result.meta_title
        title = parse_result.project if target_file.stem.lower() == "index" else parse_result.document_title
        html_file = parse_result.html_input_file

        preamble = self._preamble(title, meta_title)

        toc = self._toc_gen.generate_toc_for(html_file)
        content = []

        if parse_result.used_snippet_formats:
            # for rst containing htmls we create a mixed (raw html + rst block) rst
            self._logger.debug(f"writing mixed rst for {parse_result.html_input_file}")
            content.extend(self._mixed_rst(tree))
        else:
            # for normal (non-rst-containing) htmls we create a raw html import rst
            self._logger.debug(f"writing raw placeholder rst for {parse_result.html_input_file}")
            content.extend(self._raw_placeholder_rst(html_file))

        # get meta directive with hash of HTML file
        meta_directive_for_htm_hash = self._create_meta_directive_for_html_hash(html_hash)

        file_content = chain(meta_directive_for_htm_hash, preamble, toc, self._containerd(content))

        write_file(target_file, file_content)

        return target_file

    def _preamble(self, title: str, meta_title: str) -> Iterator[str]:
        _safe_title = self._rst_safe_encode(title)
        # _safe_meta_title = self._rst_safe_encode(meta_title)
        # an encoding in meta title isn't needed because it's text seems to be not
        # rst-interpreted

        yield ":orphan:"
        yield ""
        yield f".. title:: {meta_title}"
        yield ""
        yield f"{_safe_title}"
        yield "=" * len(_safe_title)
        yield ""

    def _create_meta_directive_for_html_hash(self, html_hash: str) -> Iterator[str]:
        """Create a meta data directive with hash of the html.

        :param html_hash: hash of the HTML file
        :yield: meta directive to be added at the top of rst file
        """
        yield f".. meta::{html_hash}"
        yield ""

    @staticmethod
    def _containerd(content: List[str]) -> Iterator[str]:
        """
        Will create a div around all the content in the final sphinx html output.

        We will use this for css scoping in the :class:`resource_provider`
        """
        yield ".. container:: doxygen-content"
        yield ""
        yield from ["   " + line for line in content]

    def _raw_placeholder_rst(self, html_file: Path) -> List[str]:
        """
        Write a rst "placeholder" file with "raw" directive to include the html directly.

        If a html file doesn't contain any @rst comments this will be used.
        """
        content = self._raw_directive(html_file.name)

        return content

    def _mixed_rst(self, tree: _ElementTree) -> List[str]:
        """
        Write a "mixed content" rst file.

        Uses "raw" directives to write HTML snippets
        broken up by native RST snippets.

        So the final file will have the original html file content represented as "raw"
        directives but any containing @rst comment will end up rendered "natively".
        """
        # get html as string
        html_string = etree.tostring(tree, encoding="unicode", method="html")

        # join adjacent rst blocks
        normalized_html_string = self._rst_join_regex.sub("", html_string)

        # split html one line each (our following algorithm is line oriented...)
        lines = normalized_html_string.split("\n")

        # iterate over all lines converting html to raw_html directives and
        # rst blocks to rst
        line_iter: Iterator[str] = iter(lines)

        content: List[str] = self._raw_directive()
        self._iterate_html(line_iter, content)

        return content

    @staticmethod
    def _raw_directive(filename: Union[str, None] = None) -> List[str]:
        """
        Return a rst raw html directive as snippet.

        When a filename is given a raw directive that includes a whole file
        (via file-attribute) is written, else content should be appended afterwards.
        """
        content: List[str] = []  # noqa F541
        if filename:
            content.append("")
        content.extend([".. raw:: html", f"  :file: {filename}" if filename else ""])
        return content

    def _iterate_html(self, line_iter: Iterator[str], content: List[str]):
        """
        Iterate over html lines.

        This is the main html processing loop.
        Once a rst node is found we switch to rst processing behavior
        (and back afterwards).

        As having empty/new lines in raw html directives isn't possible
        (because newlines would start a new block and end the raw block) we need to
        buffer the output to be able to write it as one line in one go.
        """
        buffer = ""  # a buffer for collecting html content
        while True:
            try:
                current = next(line_iter)

                if match := self._rst_element_regex.match(current):
                    content.append(f"  {buffer}")
                    buffer = ""
                    snippet_type = match.group("type")
                    if snippet_type == "rst:inline":
                        inline_rst = match.group("inline_content")
                        self._append_inline_rst_and_prefix(inline_rst, content)
                        content.extend(self._raw_directive())
                        # self._iterate_rst(line_iter, content)
                        # this is done by _iterate_rst isn't it? -> content.extend(self._raw_directive())
                    else:
                        self._iterate_rst(line_iter, content)
                else:
                    buffer += current
            except StopIteration:
                break
        content.append(f"  {buffer}")

    def _append_inline_rst_and_prefix(self, inline_content: str, content: List[str]):
        decoded_line = html.unescape(inline_content.strip())
        last_content_line = content.pop()
        if last_content_line.endswith(" "):
            last_content_line = f"{last_content_line[:-1]}&nbsp;"
        # last_content_line += '<em class="doxysphinx-inline-rst-content-before-marker"> </em>'
        content.append(last_content_line)
        content.append("")
        content.append(f"{decoded_line}")
        content.append("")

    # def _append_inline_rst_and_prefix(self, inline_content: str, content: List[str]):
    #     decoded_line = html.unescape(inline_content.strip())
    #     content.append("")
    #     # content.append(".. container:: doxysphinx-inline-rst-content-before-marker")
    #     # content.append("")
    #     # content.append("   dummy")
    #     # content.append("")
    #     content.append(".. container:: doxysphinx-inline-content-wrapper")
    #     content.append("")
    #     content.append(f"   {decoded_line}")
    #     content.append("")

    def _iterate_rst(self, line_iter: Iterator[str], content: List[str]):
        """Iterate over rst lines."""
        content.append("")
        buffer = ""  # a buffer for collecting rst content...
        # note that we need to collect the whole rst snippet as single string with
        # newline characters to apply the dedent function.
        while True:
            try:
                current = next(line_iter)
                if current.strip().startswith("</snippet>"):
                    # dedent buffer and convert it to lines
                    dedented_buffer = dedent(buffer)
                    buffer_lines = dedented_buffer.split("\n")
                    decoded_buffer_lines = [html.unescape(line) for line in buffer_lines]
                    # we need to decode the html or else we cannot use chars like
                    # "<",">" etc. (e.g. when creating external links in rst)
                    content.extend(decoded_buffer_lines)
                    content.extend(self._raw_directive())
                    break
                buffer += current + "\n"
            except StopIteration as exc:
                raise RuntimeError(
                    "End of input-file reached during rst processing. This should never "
                    "happen. Either this tool has a bug or the doxygen input file has a "
                    "severe problem."
                ) from exc
