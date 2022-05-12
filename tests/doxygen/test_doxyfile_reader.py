# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from typing import Tuple

import pytest

from doxysphinx.doxygen import _parse_key_val


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
def test_doxyfile_reader_parse_key_va(input_line: str, expected: Tuple[str, str]):
    assert _parse_key_val(input_line) == expected
