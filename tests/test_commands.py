# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path

from click.testing import CliRunner

from doxysphinx.cli import cli
from doxysphinx.utils.pathlib_fix import path_resolve


def test_build_is_working_as_expected():
    """Check if the build is working as expected"""
    runner = CliRunner()
    repo_root = path_resolve(Path())

    sphinx_source = repo_root
    sphinx_output = repo_root / ".build/html"
    doxyfile = repo_root / "demo" / "demo.doxyfile"

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert (repo_root / "pyproject.toml").exists()
    if result.exit_code != 0:
        print("Build had errors - std output stream:")
        print(result.stdout)
    assert result.exit_code == 0
    print("test2")
    assert (repo_root / ".build/html/docs/doxygen/demo/html/doxygen.css").exists()
    print("test3")


def test_incremental_build_working_as_expected():
    """Check incremental behaviour"""
    runner = CliRunner()
    repo_root = path_resolve(Path())

    sphinx_source = repo_root
    sphinx_output = repo_root / ".build/html"
    doxyfile = repo_root / "demo" / "demo.doxyfile"

    result = runner.invoke(
        cli,
        ["--verbosity=DEBUG", "clean"],
    )

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )

    result = runner.invoke(
        cli,
        [
            "--verbosity=DEBUG",
            "build",
            str(sphinx_source),
            str(sphinx_output),
            str(doxyfile),
        ],
    )
    assert "created 0 rst-files" in result.stdout
