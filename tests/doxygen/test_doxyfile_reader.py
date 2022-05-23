# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

import os
from typing import Tuple

import pytest

from doxysphinx.doxygen import _expand_envvars, _parse_key_val


@pytest.mark.parametrize(
    "input_line, expected",
    [
        (
            "OUTPUT_DIRECTORY=/workspaces/doxysphinx/docs/doxygen",
            ("OUTPUT_DIRECTORY", "/workspaces/doxysphinx/docs/doxygen"),
        ),
        (
            "OUTPUT_DIRECTORY='/workspaces/doxysphinx/docs/doxygen'",
            ("OUTPUT_DIRECTORY", "/workspaces/doxysphinx/docs/doxygen"),
        ),
        (
            "OUTPUT_DIRECTORY=" "/workspaces/doxysphinx/docs/doxygen" "",
            ("OUTPUT_DIRECTORY", "/workspaces/doxysphinx/docs/doxygen"),
        ),
        (
            'OUTPUT_DIRECTORY="/workspaces/doxysphinx/docs/doxygen"',
            ("OUTPUT_DIRECTORY", "/workspaces/doxysphinx/docs/doxygen"),
        ),
    ],
)
def test_doxyfile_reader_parse_key_val(input_line: str, expected: Tuple[str, str]):
    assert _parse_key_val(input_line) == expected


@pytest.mark.parametrize(
    "original_val, expanded_val",
    [
        ("This is a Test string without any expansions.", "This is a Test string without any expansions."),
        ("This is a $(TEST).", "This is a test_expansion."),
        # these are NOT working (because doxygen also isn't supporting these...):
        ("This is a ${TEST}.", "This is a ${TEST}."),
        ("This is a $TEST.", "This is a $TEST."),
    ],
)
def test_doxyfile_reader_expand_env_vars(original_val: str, expanded_val):
    os.environ["TEST"] = "test_expansion"
    assert _expand_envvars(original_val) == expanded_val
