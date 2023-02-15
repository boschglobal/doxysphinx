# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path

import doxygen_testfiles.config_dict_result
import pytest

from doxysphinx.doxygen import ConfigDict, _parse_stdout


@pytest.mark.parametrize(
    "input_line, expected",
    [
        (
            "OUTPUT_DIRECTORY=/workspaces/doxysphinx/docs/doxygen",
            {"OUTPUT_DIRECTORY": "/workspaces/doxysphinx/docs/doxygen"},
        ),
        (
            "OUTPUT_DIRECTORY='/workspaces/doxysphinx/docs/doxygen'",
            {"OUTPUT_DIRECTORY": "/workspaces/doxysphinx/docs/doxygen"},
        ),
        (
            "OUTPUT_DIRECTORY=" "/workspaces/doxysphinx/docs/doxygen" "",
            {"OUTPUT_DIRECTORY": "/workspaces/doxysphinx/docs/doxygen"},
        ),
        (
            'OUTPUT_DIRECTORY="/workspaces/doxysphinx/docs/doxygen"',
            {"OUTPUT_DIRECTORY": "/workspaces/doxysphinx/docs/doxygen"},
        ),
    ],
)
def test_doxyfile_reader_parsing_paths(input_line: str, expected: ConfigDict):
    assert _parse_stdout(input_line) == expected


@pytest.mark.parametrize(
    "load_input",
    [
        (Path("tests/doxygen/doxygen_testfiles/unix_line_endings.doxyfile")),
        (Path("tests/doxygen/doxygen_testfiles/windows_line_endings.doxyfile")),
    ],
    indirect=True,
)
def test_doxyfile_reader_lineendings_workasexpected(load_input, expected_config: ConfigDict):
    assert _parse_stdout(load_input) == expected_config


@pytest.fixture
def load_input(request):
    return request.param.read_text()


@pytest.fixture
def expected_config():
    return doxygen_testfiles.config_dict_result.config_dict
