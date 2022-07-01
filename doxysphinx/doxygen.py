# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
#  - Celina Adelhardt, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The doxygen module contains classes and functions specific to doxygen."""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import json5

from doxysphinx.utils.pathlib_fix import path_is_relative_to


def read_doxyfile(doxyfile: Path) -> Dict[str, str]:
    """
    Read doxygen configuration file and returns the configuration key value pairs as dict.

    :param doxyfile: the doxygen configuration file to read
    :return: a dict representing all key value pairs defined in doxyfile.
    """
    lines: List[str] = doxyfile.read_text().split("\n")
    pairs = [_parse_key_val(line) for line in lines if _is_config_line(line)]
    return dict(pairs)


def _is_config_line(line: str) -> bool:
    normalized_line = line.strip()

    # false for comments
    if normalized_line.startswith("#"):
        return False

    # true for lines with = in it
    if "=" in normalized_line:
        return True

    # false for everything else
    return False


def _parse_key_val(line: str) -> Tuple[str, str]:
    segments = line.split("=")
    key = segments[0].strip().strip("'\"")
    value = _expand_envvars(segments[1].strip().strip("'\""))
    return key, value


def _expand_envvars(val: str) -> str:
    """Expand environment variables with doxygen pattern style with normal parentheses, e.g. "$(ENV_VARIABLE)".

    :param val: The value to search and expand
    :return: The expanded or original value
    """
    # short circuit if no env var is present
    if "$(" not in val:
        return val

    # just replace doxygen env delimiters with python delimiters and format/replace with env.
    # this is just a poor mans
    return val.replace("$(", "{").replace(")", "}").format(**os.environ)


class DoxygenSettingsValidator:
    """
    Validate doxygen settings for compatibility with doxysphinx.

    Doxysphinx requires some settings to be present/set in a specific way.
    """

    mandatory_settings = {
        "OUTPUT_DIRECTORY": "",
        "SEARCHENGINE": "NO",
        "GENERATE_TREEVIEW": "NO",
        "DISABLE_INDEX": "NO",
        "ALIASES": "rst",
        "endrst": "\\endverbatim",
        "GENERATE_HTML": "YES",
        "GENERATE_TAGFILE": "",
        "CREATE_SUBDIRS": "NO",
    }
    """
    A dictionary containing mandatory settings for the doxygen config.
    The values of OUTPUT_DIRECTORY and GENERATE_TAGFILE will be set after instantiation and validation of the filepaths.
    """

    optional_settings = {
        "GENERATE_XML": "NO",
        "DOT_IMAGE_FORMAT": "svg",
        "DOT_TRANSPARENT": "YES",
        "INTERACTIVE_SVG": "YES",
        "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
    }
    """A dictionary containing further optional settings for the doxygen config."""

    def validate_doxygen_config(self, settings: Dict[str, str]) -> Dict[str, Tuple[str, str]]:
        """Validate doxygen settings regarding the mandatory settings.

        :param settings: Imported doxygen settings from doxyfile.
        :return: Empty dictionary if the validation was successful,
        dictionary containing the wrong doxygen settings and needed values if not and doxysphinx should exit.
        """
        return check_settings(settings, "mandatory")

    def validate_doxygen_out_dirs(self, out_dir: Path, sphinx_source_dir: Path) -> bool:
        """
        Validate the output directory given from doxyfile.

        :param out_dir: output directory value in doxyfile.
        :param sphinx_source_dir: sphinx docs source-directory.
        :return: True if doxygen output directory is located inside the sphinx docs root,
        False if not and doxysphinx should exit.
        """
        if path_is_relative_to(out_dir, sphinx_source_dir):
            return True
        else:
            return False

    def validate_doxygen_recommended_settings(self, settings: Dict[str, str]) -> Dict[str, Tuple[str, str]]:
        """Check if doxyfile contains the recommended settings with its values.

        :param settings: doxygen settings from doxyfile.
        :return: True if the settings have the recommended values, False if not to create a warning.
        """
        return check_settings(settings, "optional")


def check_settings(imported_settings: Dict[str, str], setting_type: str) -> Dict[str, Tuple[str, str]]:
    """Compare the imported doxygen settings with mandatory or recommended settings.

    :param imported_settings: Parsed doxygen settings from doxyfile.
    :param target_settings: Hardcoded dicts with reference values, either mandatory_settings or optional_settings.
    :return: Empty dictionary if the validation was successful, else dictionary containing the wrong
    doxygen settings and needed values in case one needs to adapt the doxygen config.
    """
    if setting_type == "mandatory":
        target_settings = DoxygenSettingsValidator.mandatory_settings
    else:
        target_settings = DoxygenSettingsValidator.optional_settings

    if all(item in imported_settings.items() for item in target_settings.items()):
        return {}
    else:
        diffs = {}
        contained_settings_target = {
            key: value for key, value in imported_settings.items() if key in target_settings.keys()
        }

        missing_imported_settings = target_settings.keys() - contained_settings_target.keys()
        if len(missing_imported_settings) > 0:
            diffs.update({key: ("missing value", target_settings[key]) for key in missing_imported_settings})

        for key in contained_settings_target.keys():
            if not contained_settings_target[key] == target_settings[key]:
                diffs[key] = (contained_settings_target[key], target_settings[key])

        return diffs


def read_js_data_file(js_data_file: Path) -> Any:
    """
    Read a doxygen javascript data file (e.g. menudata.js) and returns the data as json structure.

    :param js_data_file: The doxygen js data file to use.
    :return: a json like dict of the data.
    """
    data = js_data_file.read_text(encoding="utf-8")
    sanitized = re.sub(r"var .*=", "", data)
    result: Any = json5.loads(sanitized)
    return result
