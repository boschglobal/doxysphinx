# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path

from click.testing import CliRunner
from doxysphinx.cli import cli
from doxysphinx.utils.pathlib_fix import path_resolve


def test_build_is_working_as_expected():
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
    print("test1")
    assert result.exit_code == 0
    print("test2")
    assert (
        repo_root / ".build/html/docs/doxygen/demo/html/doxygen.css"
    ).exists()
    print("test3")
