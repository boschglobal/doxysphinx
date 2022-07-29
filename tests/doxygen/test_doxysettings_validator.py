# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Celina Adelhardt, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

import os
from pathlib import Path
from typing import Dict, List

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
                "HTML_OUTPUT": "html",
                "GENERATE_XML": "NO",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            [],  # correct input with another order
        ),
        (
            {
                "OUTPUT_DIRECTORY": "docs/doxygen/demo",
                "GENERATE_TREEVIEW": "NO",
                "ALIASES": "rst",
                "DISABLE_INDEX": "NO",
                "GENERATE_HTML": "YES",
                "endrst": "\\endverbatim",
                "GENERATE_TAGFILE": "docs/doxygen/demo/tagfile.xml",
                "CREATE_SUBDIRS": "NO",
                "SEARCHENGINE": "NO",
                "GENERATE_XML": "NO",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            [],  # missing html_output
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
                "HTML_OUTPUT": "html",
                "GENERATE_XML": "NO",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            ["Hint: Wrong value no for SEARCHENGINE, NO is recommended."],  # one param in lower case
        ),
        (
            {
                "OUTPUT_DIRECTORY": "docs/doxygen/demo",
                "SEARCHENGINE": "NO",
                "GENERATE_TREEVIEW": "NO",
                "ALIASES": "rst",
                "endrst": "\\endverbatim",
                "DISABLE_INDEX": "YES",
                "GENERATE_HTML": "NO",
                "GENERATE_TAGFILE": "docs/doxygen/demo/html/tagfile.xml",
                "CREATE_SUBDIRS": "NO",
                "HTML_OUTPUT": "html",
                "GENERATE_XML": "YES",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            [
                "Error: Wrong value YES for DISABLE_INDEX, NO is required.",
                "Error: Wrong value NO for GENERATE_HTML, YES is required.",
                "Hint: Wrong value YES for GENERATE_XML, NO is recommended.",
            ],  # two mandatory settings and one optional setting are wrong
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
                "HTML_OUTPUT": "html",
                "GENERATE_XML": "NO",
                "DOT_IMAGE_FORMAT": "svg",
                "HTML_OUTPUT": "html",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
            },
            [
                "Error: Missing value for DISABLE_INDEX, but NO is required.",
                "Hint: Missing value for HTML_EXTRA_STYLESHEET, but YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css is recommended.",
            ],  # two settings are missing (instead another flag is present),
        ),
        (
            {
                "OUTPUT_DIRECTORY": "/em-hackathon/code",
                "SEARCHENGINE": "NO",
                "GENERATE_TREEVIEW": "NO",
                "RANDOM_FLAG": "YES",
                "DISABLE_INDEX": "NO",
                "HTML_OUTPUT": "html",
                "GENERATE_HTML": "YES",
                "ALIASES": "rst",
                "endrst": "\\endverbatim",
                "CREATE_SUBDIRS": "NO",
                "GENERATE_TAGFILE": "/em-hackathon/code/html/tagfile.xml",
                "GENERATE_XML": "NO",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            [
                'The doxygen OUTPUT_DIR of "/em-hackathon/code/html" defined in the doxyfile'
                f' is not in a sub-path of the sphinx source directory "{Path(os.getcwd())}".'
            ],  # wrong output directory
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
                "GENERATE_TAGFILE": "docs/doxygen/tagfile.xml",
                "ANOTHER_FLAG": "YES",
                "ANOTHER_TAG": "NO",
                "GENERATE_XML": "NO",
                "DOT_IMAGE_FORMAT": "svg",
                "DOT_TRANSPARENT": "YES",
                "INTERACTIVE_SVG": "YES",
                "HTML_OUTPUT": "html",
                "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
            },
            [
                "Hint: Wrong value docs/doxygen/tagfile.xml for GENERATE_TAGFILE, docs/doxygen/demo/html/tagfile.xml is recommended.",
            ],  # additional flags in doxyfile & another path for tagfiile
        ),
    ],
)
def test_doxysettings_validation(validator, working_directory, test_input: Dict[str, str], expected: List[str]):
    validator.validation_errors.clear()
    validator.validate(test_input, working_directory)
    assert validator.validation_errors == expected


@pytest.fixture
def validator():
    validator = Validator()
    return validator


@pytest.fixture
def working_directory():
    return Path(os.getcwd())
