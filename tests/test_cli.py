# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from click.testing import CliRunner
from doxysphinx.cli import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0

    # just take any line from the root command docs and see if its part of the output
    assert "Doxysphinx typically should run right after doxygen." in result.output
