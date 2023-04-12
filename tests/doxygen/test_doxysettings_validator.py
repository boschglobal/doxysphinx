# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Celina Adelhardt, :em engineering methods AG (contracted by Robert Bosch GmbH)
#  - Gergely Meszaros, Stream HPC B.V. (contracted by Advanced Micro Devices Inc.)
# =====================================================================================

from pathlib import Path
from typing import List

import pytest

from doxysphinx.doxygen import ConfigDict
from doxysphinx.doxygen import DoxygenOutputPathValidator as Path_Validator
from doxysphinx.doxygen import DoxygenSettingsValidator as Validator

default_dict = {
    "OUTPUT_DIRECTORY": "docs/doxygen/demo",
    "GENERATE_TREEVIEW": "NO",
    "ALIASES": ["rst=\\verbatim embed:rst:leading-asterisk", "endrst=\\endverbatim"],
    "DISABLE_INDEX": "NO",
    "GENERATE_HTML": "YES",
    "GENERATE_TAGFILE": "docs/doxygen/demo/html/tagfile.xml",
    "CREATE_SUBDIRS": "NO",
    "SEARCHENGINE": "NO",
    "HTML_OUTPUT": "html",
    "GENERATE_XML": "NO",
    "DOT_IMAGE_FORMAT": "svg",
    "DOT_TRANSPARENT": "YES",
    "INTERACTIVE_SVG": "YES",
    "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
}


def update_dict(params: ConfigDict):
    dict = default_dict.copy()
    dict.update(params)
    return dict


@pytest.mark.parametrize(
    "test_dict, expected_validation_errors",
    [
        (
            default_dict,
            [],  # correct input with another order
        ),
        (
            update_dict({"SEARCHENGINE": "no"}),
            ["Hint: Wrong value no for SEARCHENGINE, NO is recommended."],  # one param in lower case
        ),
        (
            update_dict({"DISABLE_INDEX": "YES", "GENERATE_HTML": "NO", "GENERATE_XML": "YES"}),
            [
                "Error: Wrong value YES for DISABLE_INDEX, NO is required.",
                "Error: Wrong value NO for GENERATE_HTML, YES is required.",
            ],  # two mandatory settings and one optional setting are wrong
        ),
        (
            {
                key: default_dict[key]
                for key in default_dict.copy()
                if key not in ["DISABLE_INDEX", "HTML_EXTRA_STYLESHEET"]
            },
            [
                "Error: Missing value for DISABLE_INDEX, but NO is required.",
            ],  # two settings are missing
        ),
        (
            update_dict({"OUTPUT_DIRECTORY": "/em-hackathon/code"}),
            [
                f'The doxygen OUTPUT_DIR of "{"/em-hackathon/code" + "/html"}" defined in the doxyfile'
                f' is not in a sub-path of the sphinx source directory "{Path.cwd()}".'
            ],  # wrong output directory
        ),
        (
            update_dict(
                {
                    "GENERATE_TAGFILE": "docs/doxygen/tagfile.xml",
                    "ANOTHER_FLAG": "YES",
                    "ANOTHER_TAG": "NO",
                }
            ),
            [
                "Hint: Wrong value docs/doxygen/tagfile.xml for GENERATE_TAGFILE, docs/doxygen/demo/html/tagfile.xml is recommended.",
            ],  # additional flags in doxyfile & another path for tagfiile
        ),
    ],
)
def test_doxysettings_validation(
    validator, working_directory, test_dict: ConfigDict, expected_validation_errors: List[str]
):
    validator.validation_errors.clear()
    validator.validate(test_dict, working_directory, working_directory)
    assert validator.validation_errors == expected_validation_errors


@pytest.fixture
def validator():
    validator = Validator()
    return validator


@pytest.fixture
def working_directory():
    return Path.cwd()


@pytest.mark.parametrize(
    "doxygen_html_output, validation_result", [(Path("docs/doxygen/demo/html"), True), (Path("docs/resources"), False)]
)
def test_doxyoutput_path_validation(path_validator, doxygen_html_output: Path, validation_result: bool):
    assert path_validator.validate(doxygen_html_output) == validation_result


@pytest.fixture
def path_validator():
    path_validator = Path_Validator()
    return path_validator
