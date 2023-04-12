# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path
from subprocess import run

import pytest


@pytest.fixture(scope="session", autouse=True)
def run_doxygen_fixture():
    run_doxygen()


def run_doxygen():
    """Run doxygen before executing any test.

    I know this isn't superb style to depend the test on some tools that's running before
    (and that takes some seconds to do it's work), however this makes especially testing the path
    mapping functions far easier...
    """
    print("running doxygen...")
    root = Path(__file__).parent / ".."
    doxyfile = (root / "demo" / "demo.doxyfile").resolve()
    result = run(["doxygen", doxyfile], cwd=root)
    result.check_returncode()
    print(f"{result.stdout}\n{result.stderr}")
