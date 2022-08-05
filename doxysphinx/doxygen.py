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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import json5

from doxysphinx.utils.pathlib_fix import path_is_relative_to, path_resolve


def read_doxyfile(doxyfile: Path) -> Dict[str, str]:
    """
    Read doxygen configuration file and returns the configuration key value pairs as dict.

    :param doxyfile: the doxygen configuration file to read
    :return: a dict representing all key value pairs defined in doxyfile.
    """
    lines: List[str] = doxyfile.read_text().split("\n")
    pairs = [_parse_key_val(line) for line in lines if _is_config_line(line)]
    return dict(pairs)


ConfigDict = Dict[str, Union[str, List[str]]]


@dataclass(frozen=True)
class DoxyOutput:
    out: str
    err: str


def read_doxyconfig(doxyfile: Path) -> ConfigDict:
    """Supplement the doxygen configuration file with the default doxygen configuration and
    return the final key value pairs as a dict.

    :param doxyfile: the doxygen configuration file to read
    :return: a dict representing all key value pairs defined in the final configuration.
    The value can either be a single value or a list.
    """
    output = _compare_configs(doxyfile)
    config = _parse_stdout(output.out)
    warnings = _parse_stderr(output.err)
    # add warnings to config dict
    config["WARNINGS"] = warnings
    return config


def _parse_stdout(text: str) -> ConfigDict:
    from pyparsing import (
        Combine,
        FollowedBy,
        Group,
        Keyword,
        LineEnd,
        LineStart,
        Literal,
        ParserElement,
        SkipTo,
        Suppress,
        Word,
        delimited_list,
        printables,
        srange,
    )

    # remove comment lines
    lines: List[str] = text.split("\n")
    clean_out = "\n".join([line for line in lines if _is_config_line(line)])

    # define the grammar
    ParserElement.set_default_whitespace_chars(" \t")

    doxy_flag = LineStart() + Word(srange("[A-Z_]")) + FollowedBy("=")

    list_items = delimited_list(Word(printables), Literal("\\\n"))
    doxy_list = doxy_flag + Suppress("=") + list_items

    normal_item = Suppress("=") + SkipTo(LineEnd())
    doxy_pair = doxy_flag + Suppress("=") + normal_item
    # aliases flag
    config_block = doxy_list | doxy_pair
    # normal_item = SkipTo(Literal("\n") + (FollowedBy(flag) | StringEnd()))
    aliases_flag = LineStart() + Keyword("ALIASES") + FollowedBy("=")
    aliases_val = Combine(Word(printables) * 2, adjacent=False, join_string=" ") + Suppress(
        Group(Literal("\\") + LineEnd())
    )
    aliases_pair = aliases_flag + Suppress("=") + aliases_val + SkipTo(LineEnd())
    aliases = aliases_pair.search_string(clean_out).asList()
    result = config_block.search_string(clean_out).asList()

    # delete alias in result and replace it with separate result
    for i in range(len(result)):
        if result[i][0] == "ALIASES":
            result[i][1] = aliases[0][1:]
        # check length of lists and optimize the format
        if len(result[i]) > 2:
            flag = result[i][0]
            vals = result[i][1:]
            result[i] = [flag, vals]

    # convert result to dict
    config_dict = {item[0]: item[1] for item in result}

    return config_dict


def _parse_stderr(text: str) -> List[str]:

    lines = text.split("\n")
    return [line.replace("warning", "Hint") for line in lines if line]


def _compare_configs(doxyfile: Path) -> DoxyOutput:
    from subprocess import CalledProcessError, run  # nosec: B404

    try:
        temp_result = run(["doxygen", "-s", "-g", "-"], capture_output=True)  # nosec: B607, B603
        if temp_result.check_returncode:
            result = run(["doxygen", "-x", f"{doxyfile}"], capture_output=True)  # nosec: B607, B603
            result.check_returncode

        return DoxyOutput(result.stdout.decode("utf-8"), result.stderr.decode("utf-8"))

    except CalledProcessError as err:
        return DoxyOutput("", f"Error: {err}")


def _is_config_line(line: str) -> bool:
    normalized_line = line.strip()

    # false for comments
    if normalized_line.startswith("#"):
        return False

    return True


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
        "GENERATE_TREEVIEW": "NO",
        "DISABLE_INDEX": "NO",
        "ALIASES": "rst",
        "endrst": "\\endverbatim",
        "GENERATE_HTML": "YES",
        "CREATE_SUBDIRS": "NO",
    }
    """
    A dictionary containing mandatory settings for the doxygen config.
    The values of OUTPUT_DIRECTORY and GENERATE_TAGFILE will be set after instantiation and validation of the filepaths.
    """

    optional_settings = {
        "SEARCHENGINE": "NO",
        "GENERATE_XML": "NO",
        "DOT_IMAGE_FORMAT": "svg",
        "DOT_TRANSPARENT": "YES",
        "INTERACTIVE_SVG": "YES",
        "HTML_EXTRA_STYLESHEET": "YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css",
        "GENERATE_TAGFILE": "",
    }
    """A dictionary containing further optional settings for the doxygen config."""

    validation_errors: List[str] = []
    """List of the validation errors including the doxyflag with its used and the correct value."""
    absolute_out: Path
    """Absolute path of the output directory."""
    validation_msg = ""
    """Validation errors merged in one string."""

    def validate(self, config: ConfigDict, sphinx_source_dir: Path) -> bool:
        """Validate the doxygen configuration regarding the output directory, mandatory and optional settings.

        :param config: the imported doxyfile.
        :param sphinx_source_dir: the sphinx directory (necessary for output directory validation).
        :return: False, if there is a deviation to the defined mandatory or optional settings.
        """
        if "WARNINGS" in config:
            self.validation_errors.extend(config["WARNINGS"])

        out_dir_validated = self._validate_doxygen_out_dirs(config, sphinx_source_dir)
        recommended_settings_validated = self._validate_doxygen_recommended_settings(config)
        optional_settings_validated = self._validate_doxygen_optional_settings(config)
        if out_dir_validated and recommended_settings_validated and optional_settings_validated:
            self.validation_msg = "All doxygen settings are set correctly."
            return True
        else:
            for error in self.validation_errors:
                self.validation_msg += error + "\n"
            return False

    def _validate_doxygen_out_dirs(self, config: ConfigDict, sphinx_source_dir: Path) -> bool:
        """
        Validate the output directory given from doxyfile and set the required values in mandatory settings.

        :param out_dir: output directory value in doxyfile.
        :param sphinx_source_dir: sphinx docs source-directory.
        :return: True if doxygen output directory is located inside the sphinx docs root,
        False if not and doxysphinx should exit.
        """

        out = Path(str(config["OUTPUT_DIRECTORY"])) / "html"  # config["HTML_OUTPUT"]
        self.absolute_out = path_resolve(out)
        stringified_out = str(out) if out.is_absolute() else f'"{out}" (resolved to "{self.absolute_out}")'

        self.mandatory_settings["OUTPUT_DIRECTORY"] = str(config["OUTPUT_DIRECTORY"])
        self.optional_settings["GENERATE_TAGFILE"] = str(out) + "/tagfile.xml"

        if path_is_relative_to(out, sphinx_source_dir):
            return True
        else:
            self.validation_errors.append(
                f'The doxygen OUTPUT_DIR of "{stringified_out}" defined in the doxyfile'
                f' is not in a sub-path of the sphinx source directory "{sphinx_source_dir}".'
            )
            return False

    def _validate_doxygen_recommended_settings(self, settings: ConfigDict) -> bool:
        imported_settings = settings
        target_settings = self.mandatory_settings
        validation_successful = True
        if all(item in imported_settings.items() for item in target_settings.items()):
            return validation_successful

        contained_settings_target = {
            key: value for key, value in imported_settings.items() if key in target_settings.keys()
        }

        missing_imported_settings = target_settings.keys() - contained_settings_target.keys()
        if missing_imported_settings:
            for key in missing_imported_settings:
                self.validation_errors.append(
                    (f"Error: Missing value for {key}, but {target_settings[key]} is required.")
                )
            validation_successful = False

        for key in contained_settings_target.keys():
            if not contained_settings_target[key] == target_settings[key]:
                self.validation_errors.append(
                    (
                        f"Error: Wrong value {contained_settings_target[key]} for {key}, {target_settings[key]} is required."
                    )
                )
                validation_successful = False

        return validation_successful

    def _validate_doxygen_optional_settings(self, settings: ConfigDict) -> bool:
        imported_settings = settings
        target_settings = self.optional_settings
        validation_successful = True
        if all(item in imported_settings.items() for item in target_settings.items()):
            return validation_successful

        contained_settings_target = {
            key: value for key, value in imported_settings.items() if key in target_settings.keys()
        }

        missing_imported_settings = target_settings.keys() - contained_settings_target.keys()
        if missing_imported_settings:
            for key in missing_imported_settings:
                self.validation_errors.append(
                    (f"Hint: Missing value for {key}, but {target_settings[key]} is recommended.")
                )
            validation_successful = False

        for key in contained_settings_target.keys():
            if not contained_settings_target[key] == target_settings[key]:
                self.validation_errors.append(
                    (
                        f"Hint: Wrong value {contained_settings_target[key]} for {key}, {target_settings[key]} is recommended."
                    )
                )
                validation_successful = False

        return validation_successful


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


class DoxygenOutputPathValidator:
    """Validates doxygen html output paths."""

    def __init__(self) -> None:
        """Create an instance of DoxygenOutputPathValidator."""
        self.validation_msg: str = ""

    def validate(self, doxygen_html_output: Path) -> bool:
        """Validate a doxygen html output path.

        This is just meant to catch typos in paths etc. It will just check if a "doxygen.css" file is existing
        In the html output path.

        :param doxygen_html_output: The path where doxygen generates its' html file to.
        :return: True if the path is valid else false.
        """
        svg_exists = (doxygen_html_output / "doxygen.css").exists()
        if not svg_exists:
            self.validation_msg = (
                f'The directory "{doxygen_html_output}" seems to be no valid doxygen html output '
                "(we're checking for existance of \"doxygen.css\" and weren't able to find it there)."
            )
        return svg_exists
