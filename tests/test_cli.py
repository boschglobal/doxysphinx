# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path

import pytest
from click import ClickException
from click.testing import CliRunner

from doxysphinx.cli import _get_outdir_via_doxyoutputdir, cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0

    # just take any line from the root command docs and see if its part of the output
    assert "Doxysphinx typically should run right after doxygen." in result.output


def test_get_outdir_via_doxyoutputdir_with_valid_doxygen_html_output_works_as_expected():
    doxygen_output_path = Path.cwd() / "docs/doxygen/demo/html"
    assert _get_outdir_via_doxyoutputdir(doxygen_output_path) == doxygen_output_path


def test_get_outdir_via_doxyoutputdir_throws_on_non_doxygen_html_output_dirs():
    with pytest.raises(ClickException) as exc:
        non_doxygen_output_path = Path.cwd() / "tests"
        _get_outdir_via_doxyoutputdir(non_doxygen_output_path)
    assert "seems to be no valid doxygen html output" in str(exc.value)
