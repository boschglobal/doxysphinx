# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path

import pytest

from doxysphinx.utils.pathlib_fix import path_is_relative_to


# @pytest.mark.skip(
#     reason="This will sometimes fail on python 3.8.X - but at present we've got no idea why. Maybe this "
#     "has something to do with pathlib3x lib (if it was present but then got uninstalled...) "
#     "however for now we're providing a custom code fix for this problem. "
#     "This test is only for manual testing of the issue."
# )
@pytest.mark.parametrize(
    "path, relative_to",
    [
        (
            Path("/workspaces/doxysphinx/doxygen/html/test.css"),
            Path("/workspaces/doxysphinx"),
        ),
        (
            Path("/workspaces/doxysphinx/doxygen/html/test.css"),
            Path("/workspaces/doxysphinx"),
        ),
    ],
)
def test_pathlib_is_relative_to_works_as_expected(path: Path, relative_to: Path):
    assert path.is_relative_to(relative_to)


@pytest.mark.parametrize(
    "path, relative_to, expected_result",
    [
        # positive tests
        # unix absolute paths
        (
            Path("/workspaces/doxysphinx/doxygen/html/test.css"),
            Path("/workspaces/doxysphinx"),
            True,
        ),
        (
            Path("/workspaces/doxysphinx/doxygen/html/test.css"),
            Path("/workspaces/doxysphinx"),
            True,
        ),
        (
            Path("/workspaces/doxysphinx/doxygen/html/test.css"),
            Path("/workspaces/"),
            True,
        ),
        (Path("/workspaces/doxysphinx/doxygen/html/test.css"), Path("/"), True),
        (
            Path("/workspaces/doxysphinx/doxygen/html"),
            Path("/workspaces/doxysphinx"),
            True,
        ),
        (Path("/workspaces/doxysphinx/doxygen/html/"), Path("/workspaces/"), True),
        (Path("/workspaces/doxysphinx/doxygen/html"), Path("/"), True),
        # unix relative paths
        (Path("."), Path("."), True),
        (Path("./"), Path("./"), True),
        (Path("doxysphinx/doxygen/html/test.css"), Path("doxysphinx"), True),
        (Path("doxysphinx/doxygen/html/test.css"), Path("doxysphinx"), True),
        (Path("doxysphinx/doxygen/html/test.css"), Path("/"), True),
        (Path("./doxygen/html/test.css"), Path("doxygen/"), True),
        (Path("doxysphinx/doxygen/html/"), Path("/"), True),
        (Path("./doxysphinx/doxygen/html"), Path("/"), True),
        # windows absolute paths
        (Path("D:\\test\\doxysphinx"), Path("D:\\"), True),
        (Path("D:\\test\\doxysphinx"), Path("D:\\test"), True),
        (Path("D:\\test\\doxysphinx"), Path("D:\\test\\doxysphinx"), True),
        # windows relative paths
        (Path("test\\doxysphinx"), Path("test"), True),
        (Path("test\\doxysphinx"), Path("test\\doxysphinx"), True),
        # negative tests
        (Path("a"), Path("b"), False),
        (Path("a/b"), Path("b/b"), False),
        (Path("a/b/c"), Path("a/b/d"), False),
        (
            Path("/doxysphinx/doxygen/html/test.css"),
            Path("/doxysphinx-other/dir"),
            False,
        ),
        (Path("D:\\test"), Path("C:\\nothing_to_do"), False),
        (Path(".\\test\\doxysphinx"), Path("\\$/$(§"), False),
        (Path("D:\\this is only a test"), Path("C:\\lets try\\doxy sphinx"), False),
    ],
)
def test_path_is_relative_to_works_as_expected(
    path: Path, relative_to: Path, expected_result: bool
):
    assert path_is_relative_to(path, relative_to) == expected_result
