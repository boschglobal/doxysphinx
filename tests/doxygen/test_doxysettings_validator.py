# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Celina Adelhardt, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path
from typing import Dict, Tuple

import pytest

from doxysphinx.doxygen import DoxygenSettingsValidator as Validator


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "OUTPUT_DIRECTORY": "docs/doxygen/demo",
                "GENERATE_TREEVIEW": "NO",
                "ALIASES": "rst",
                "DISABLE_INDEX": "NO",
                "GENERATE_HTML": "YES",
                "endrst": "\\endverbatim",
                "GENERATE_TAGFILE": "docs/doxygen/demo/html/tagfile.xml",
                "CREATE_SUBDIRS": "NO",
                "SEARCHENGINE": "NO",
            },
            {},  # correct input with another order
        ),
        (
            {
                "OUTPUT_DIRECTORY": "docs/doxygen/demo",
                "GENERATE_TREEVIEW": "NO",
                "ALIASES": "rst",
                "DISABLE_INDEX": "NO",
                "GENERATE_HTML": "YES",
                "endrst": "\\endverbatim",
                "GENERATE_TAGFILE": "docs/doxygen/demo/html/tagfile.xml",
                "CREATE_SUBDIRS": "NO",
                "SEARCHENGINE": "no",
            },
            {"SEARCHENGINE": ("no", "NO")},  # one param in lower case
        ),
        (
            {
                "OUTPUT_DIRECTORY": "docs/doxygen/demo",
                "SEARCHENGINE": "NO",
                "GENERATE_TREEVIEW": "NO",
                "ALIASES": "rst",
                "endrst": "\\endverbatim",
                "DISABLE_INDEX": "NO",
                "GENERATE_HTML": "NO",
                "GENERATE_TAGFILE": "docs/doxygen/demo/html/tagfile.xml",
                "CREATE_SUBDIRS": "NO",
            },
            {"GENERATE_HTML": ("NO", "YES")},  # one setting is wrong
        ),
        (
            {
                "OUTPUT_DIRECTORY": "docs/doxygen/demo",
                "SEARCHENGINE": "NO",
                "GENERATE_TREEVIEW": "NO",
                "RANDOM_FLAG": "YES",
                "GENERATE_HTML": "YES",
                "ALIASES": "rst",
                "endrst": "\\endverbatim",
                "CREATE_SUBDIRS": "NO",
                "GENERATE_TAGFILE": "docs/doxygen/demo/html/tagfile.xml",
            },
            {"DISABLE_INDEX": ("missing value", "NO")},  # one setting is missing (instead another flag is present)
        ),
        (
            {
                "OUTPUT_DIRECTORY": "docs/doxygen/demo",
                "SEARCHENGINE": "NO",
                "ALIASES": "rst",
                "endrst": "\\endverbatim",
                "GENERATE_TREEVIEW": "NO",
                "DISABLE_INDEX": "NO",
                "GENERATE_HTML": "YES",
                "CREATE_SUBDIRS": "NO",
                "GENERATE_TAGFILE": "docs/doxygen/demo/html/tagfile.xml",
                "ANOTHER_FLAG": "YES",
                "ANOTHER_TAG": "NO",
            },
            {},  # additional flags in doxyfile
        ),
    ],
)
def test_doxysettings_validation(validator, test_input: Dict[str, str], expected: Dict[str, Tuple[str, str]]):
    assert validator.validate_doxygen_config(test_input) == expected


@pytest.fixture
def validator():
    validator = Validator()
    validator.mandatory_settings["OUTPUT_DIRECTORY"] = "docs/doxygen/demo"
    validator.mandatory_settings["GENERATE_TAGFILE"] = "docs/doxygen/demo/html/tagfile.xml"
    return validator


@pytest.mark.parametrize(
    "test_dir, expected",
    [
        ("/workspaces/doxysphinx/docs/doxygen", True),
        ("/workspaces/doxysphinx", False),  # test_dir is the source_dir itself
        ("~/em-hackathon/code", False),  # another directory outside the devcontainer
    ],
)
def test_doxy_out_dir_validation(validator, test_dir: str, expected: bool):
    assert validator.validate_doxygen_out_dirs(Path(test_dir), Path("/workspaces/doxysphinx"))


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "GENERATE_XML": "NO",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            {},  # correct input
        ),
        (
            {
                "GENERATE_XML": "YES",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            {"GENERATE_XML": ("YES", "NO")},  # one changed input
        ),
        (
            {
                "GENERATE_XML": "NO",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "RANDOM FLAG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            {"DOT_IMAGE_FORMAT": ("missing value", "svg")},  # one missing input & another flag
        ),
    ],
)
def test_doxy_optional_settings_validation(validator, test_input: Dict[str, str], expected: bool):
    assert validator.validate_doxygen_recommended_settings(test_input) == expected
