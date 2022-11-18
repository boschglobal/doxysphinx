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
from typing import Any, Dict, List, Union

import json5

from doxysphinx.utils.pathlib_fix import path_is_relative_to, path_resolve

ConfigDict = Dict[str, Union[str, List[str]]]


@dataclass(frozen=True)
class DoxyOutput:
    """Class to summarize the strings of the console output and error streams."""

    out: str
    err: str


def read_doxyconfig(doxyfile: Path, doxygen_exe: str, doxygen_cwd: Path) -> ConfigDict:
    """Read doxyconfig and get full doxygen configuration (also with default values).

    Supplement the doxygen configuration file with the default doxygen configuration and return the final
    key value pairs as a dict.

    :param doxyfile: the doxygen configuration file to read
    :param doxygen_exe: in case one wants to execute doxygen from another directory.
    :return: a dict representing all key-value pairs defined in the final configuration
             (including warnings from the console output). The value can either be a single value or a list.
    """
    output = _compare_configs(doxyfile, doxygen_exe, doxygen_cwd)
    config = _parse_stdout(output.out)
    config["WARNINGS"] = _parse_stderr(output.err)
    return config


def _compare_configs(doxyfile: Path, doxygen_exe: str, doxygen_cwd: Path) -> DoxyOutput:
    from subprocess import CalledProcessError, run  # nosec: B404

    try:
        default_config = run(  # nosec: B607, B603
            f"{doxygen_exe} -s -g -", cwd=doxygen_cwd, shell=True, capture_output=True  # nosec: B607, B603, B602
        )  # nosec: B607, B603
        if default_config.check_returncode:
            custom_config = run(  # nosec: B607, B603
                f"{doxygen_exe} -x {doxyfile}",
                cwd=doxygen_cwd,
                shell=True,  # nosec: B602
                capture_output=True,  # nosec: B607, B603
            )  # nosec: B607, B603
            custom_config.check_returncode

        return DoxyOutput(
            default_config.stdout.decode("utf-8") + custom_config.stdout.decode("utf-8"),
            default_config.stderr.decode("utf-8") + custom_config.stderr.decode("utf-8"),
        )

    except CalledProcessError as err:
        return DoxyOutput("", f"Error: {err}")


def _parse_stdout(text: str) -> ConfigDict:
    """Remove comment lines and parse the console output via pyparsing to a dictionary.

    :param text: standard output of the console.
    :return: a configuration dictionary with possibility of lists as values.
    """
    from pyparsing import (
        FollowedBy,
        Group,
        LineEnd,
        Literal,
        ParserElement,
        QuotedString,
        Suppress,
        White,
        Word,
        delimited_list,
        printables,
        srange,
    )

    lines: List[str] = text.split(os.linesep)
    pure_text = os.linesep.join([line for line in lines if _is_config_line(line)])

    ParserElement.set_default_whitespace_chars(" \t")
    line_end = LineEnd() if os.linesep == "\n" else White("\r\n")

    doxy_flag = Word(srange("[A-Z_]")) + FollowedBy("=")
    list_items = delimited_list(
        QuotedString('"') | QuotedString("'") | Word(printables), Group(Literal("\\") + line_end)
    )
    config_pair = doxy_flag + Suppress("=") + list_items
    config = config_pair.search_string(pure_text).asList()

    # format correcting
    for i in range(len(config)):
        if len(config[i]) > 2:
            flag = config[i][0]
            val = config[i][1:]
            config[i] = [flag, val]

    config_dict = {item[0]: item[1] for item in config}

    return config_dict


def _is_config_line(line: str) -> bool:
    normalized_line = line.strip()

    # false for comments
    if normalized_line.startswith("#"):
        return False

    return True


def _parse_stderr(text: str) -> List[str]:

    lines = text.split(os.linesep)
    return [line.replace("warning", "Hint") for line in lines if line]


class DoxygenSettingsValidator:
    """
    Validate doxygen settings for compatibility with doxysphinx.

    Doxysphinx requires some settings to be present/set in a specific way.
    """

    mandatory_settings = {
        "OUTPUT_DIRECTORY": "",
        "GENERATE_TREEVIEW": "NO",
        "DISABLE_INDEX": "NO",
        "ALIASES": ["rst=\\verbatim embed:rst:leading-asterisk", "endrst=\\endverbatim"],
        "GENERATE_HTML": "YES",
        "CREATE_SUBDIRS": "NO",
    }
    """
    A dictionary containing mandatory settings for the doxygen config.
    The values of OUTPUT_DIRECTORY and GENERATE_TAGFILE will be set after instantiation and validation of the filepaths.
    """

    optional_settings = {
        "SEARCHENGINE": "NO",
        "DOT_IMAGE_FORMAT": "svg",
        "DOT_TRANSPARENT": "YES",
        "INTERACTIVE_SVG": "YES",
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

        if path_is_relative_to(out, sphinx_source_dir):
            self.optional_settings["GENERATE_TAGFILE"] = str(out) + "/tagfile.xml"
            return True
        else:
            self.optional_settings["GENERATE_TAGFILE"] = "docs/doxygen/demo/html/tagfile.xml"  # default value
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

        :param doxygen_html_output: The path where doxygen generates its html file to.
        :return: True if the path is valid else false.
        """
        svg_exists = (doxygen_html_output / "doxygen.css").exists()
        if not svg_exists:
            self.validation_msg = (
                f'The directory "{doxygen_html_output}" seems to be no valid doxygen html output '
                "(we're checking for existance of \"doxygen.css\" and weren't able to find it there)."
            )
        return svg_exists
