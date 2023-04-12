# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path

import pytest

from doxysphinx.sphinx import SphinxHtmlBuilderDirectoryMapper
from doxysphinx.utils.pathlib_fix import path_resolve


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    ws_root_dir = path_resolve(Path(request.fspath.dirname) / ".." / "..")
    monkeypatch.chdir(ws_root_dir)


@pytest.fixture
def mapper_output_in_source_with_absolute_paths(source, output):
    source_path: Path = path_resolve(Path("./"))
    output_path: Path = path_resolve(Path("./.build"))
    return SphinxHtmlBuilderDirectoryMapper(source_path, output_path)


@pytest.fixture
def mapper_output_in_source_with_relative_paths(source, output):
    source_path: Path = Path("./")
    output_path: Path = Path("./.build")
    return SphinxHtmlBuilderDirectoryMapper(source_path, output_path)


@pytest.mark.parametrize(
    "source, output",
    [
        (Path("docs/doxygen/html/test.css"), Path(".build/docs/doxygen/html/test.css")),
        (Path("docs/doxygen/html/search"), Path(".build/docs/doxygen/html/search")),
        (Path("test.css"), Path(".build/test.css")),
        (
            Path("docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg"),
            Path(".build/docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg"),
        ),
    ],
)
def test_directory_mapper_works_with_relative_paths_variant_1(
    mapper_output_in_source_with_absolute_paths, source, output
):
    assert mapper_output_in_source_with_absolute_paths.map(source) == output


@pytest.mark.parametrize(
    "source, output",
    [
        (Path("docs/doxygen/html/test.css"), Path(".build/docs/doxygen/html/test.css")),
        (Path("docs/doxygen/html/search"), Path(".build/docs/doxygen/html/search")),
        (Path("test.css"), Path(".build/test.css")),
        (
            Path("docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg"),
            Path(".build/docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg"),
        ),
    ],
)
def test_directory_mapper_works_with_relative_paths_variant_2(
    mapper_output_in_source_with_relative_paths, source, output
):
    assert mapper_output_in_source_with_relative_paths.map(source) == output


@pytest.mark.parametrize(
    "source, output",
    [
        (
            Path.cwd() / "docs/doxygen/html/test.css",
            Path.cwd() / ".build/docs/doxygen/html/test.css",
        ),
        (
            Path.cwd() / "docs/doxygen/html/search",
            Path.cwd() / ".build/docs/doxygen/html/search",
        ),
        (Path.cwd() / "test.css", Path.cwd() / ".build/test.css"),
        (
            Path.cwd() / "docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg",
            Path.cwd() / ".build/docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg",
        ),
    ],
)
def test_directory_mapper_works_with_absolute_paths_variant_1(
    mapper_output_in_source_with_absolute_paths, source, output
):
    assert mapper_output_in_source_with_absolute_paths.map(source) == output


@pytest.mark.parametrize(
    "source, output",
    [
        (
            Path.cwd() / "docs/doxygen/html/test.css",
            Path.cwd() / ".build/docs/doxygen/html/test.css",
        ),
        (
            Path.cwd() / "docs/doxygen/html/search",
            Path.cwd() / ".build/docs/doxygen/html/search",
        ),
        (Path.cwd() / "test.css", Path.cwd() / ".build/test.css"),
        (
            Path.cwd() / "docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg",
            Path.cwd() / ".build/docs/doxygen/demo/html/classdoxysphinx_1_1rst_1_1Car__inherit__graph.svg",
        ),
    ],
)
def test_directory_mapper_works_with_absolute_paths_variant_2(
    mapper_output_in_source_with_relative_paths, source, output
):
    assert mapper_output_in_source_with_relative_paths.map(source) == output


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            Path.cwd() / "build/aca5/generated/docs/html",
            Path.cwd() / "build/aca5/generated/docs/final/build/aca5/generated/docs/html",
        ),
        (
            Path.cwd() / "build/aca5/generated/docs/final/doxygen/test.html",
            Path.cwd() / "build/aca5/generated/docs/final/build/aca5/generated/docs/final/doxygen/test.html",
        ),
    ],
)
def test_directory_mapper_works_correctly_with_simulated_pace_env(source, expected):
    mapper = SphinxHtmlBuilderDirectoryMapper(Path.cwd(), Path.cwd() / "build/aca5/generated/docs/final")
    mapped = mapper.map(Path(source))
    assert mapped == expected
