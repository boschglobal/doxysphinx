# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
#  - Stefan Schulz, itemis AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""Some helper functions for conf.py."""
import datetime
import glob
import re
from typing import Any, Dict, List

# pylint: disable=all


def version_from_project_toml() -> str:
    """Get the version number from project.toml file."""
    with open("pyproject.toml", "r") as toml:
        text = toml.read()
        matches = re.findall(r"^version = ['\"](\d+\.\d+\.\d+)['\"]", text, flags=re.MULTILINE)
        return matches[0]


def multi_glob(*glob_patterns: str) -> List[str]:
    """Expand the glob_patterns to a list of matching files/directories.

    :return: A list of matching files/directories.
    :rtype: List[str]
    """
    result = []
    for p in glob_patterns:
        for path in glob.glob(p):
            result.append(path)
    return result


def last_updated_from_git(repo_url: str) -> str:
    """Get the last updated string from git command (needs a git repository!).

    :return: The last updated string
    :rtype: str
    """
    git_cmd_timestamp = ["git", "log", "--pretty=format:'%ad'", "--date=local", "-n1"]
    git_cmd_commit = ["git", "log", "--pretty=format:'%h'", "--date=local", "-n1"]

    import subprocess  # nosec: B404

    try:
        ts = subprocess.check_output(git_cmd_timestamp).decode("utf-8")  # nosec: B603
        commit = subprocess.check_output(git_cmd_commit).decode("utf-8")  # nosec: B603
        return f"{ts}, {commit}"
    except Exception:
        return f"{datetime.datetime.now()}, <no git commit available>"


def theme_options(theme: str) -> Dict[str, Any]:
    """Get the theme options dict for a given supported theme."""
    supported_themes = ["sphinx_book_theme", "sphinx_rtd_theme"]
    if theme not in supported_themes:
        raise Exception(f"theme {theme} is not supported by doxysphinx. " f"Must be one of {supported_themes}.")

    if theme == "sphinx_book_theme":
        return {
            "show_navbar_depth": 1,
            "collapse_navigation": True,
            "repository_url": "https://github.com/boschglobal/doxysphinx",
            "use_repository_button": True,
            "use_edit_page_button": True,
            "repository_branch": "main",
            "logo_only": True,
            "home_page_in_toc": True,
            "extra_navbar": '<div class="attribution">theme based on the '
            '<a href="https://sphinx-book-theme.readthedocs.io/">sphinx book theme</a> '
            'by the <a href="https://executablebooks.org/">executable book project'
            "</a>.</div>",
        }

    elif theme == "sphinx_rtd_theme":
        return {
            "show_nav_level": 1,
            "collapse_navigation": True,
            "github_url": "https://github.com/boschglobal/doxysphinx",
            "repository_url": "https://github.com/boschglobal/doxysphinx",
            "logo_only": False,
        }
    else:
        raise Exception("this should never happen...")
