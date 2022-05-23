# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The doxygen module contains classes and functions specific to doxygen."""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import json5


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

    def validate(self, settings: Dict[str, str]) -> bool:
        """
        Validate doxygen settings.

        :param settings: doxygen settings.
        :return: True if the validation was successful, False if it wasn't and doxysphinx
                 should exit.
        """
        # warnings
        pass
        # errors


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
