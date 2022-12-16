# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

# Note:
# =====
# To use this script the graphviz docs have to be downloaded (see demos/load_additional_demos.sh)
#

import logging
from datetime import timedelta
from pathlib import Path
from typing import Iterable

from conftest import run_doxygen

from doxysphinx.process import Builder, Cleaner
from doxysphinx.utils.contexts import TimedContext


def _run_and_get_timings(iterations: int, parallel: bool) -> Iterable[timedelta]:
    root = Path(__file__).parent / ".."
    sphinx_source = root.resolve()
    sphinx_output = root / ".build" / "html"
    doxygen_html_dir = root / "demo" / "graphviz" / "doxygen" / "html"

    for i in range(iterations):
        cleaner = Cleaner(sphinx_source, sphinx_output, parallel=parallel)
        cleaner.cleanup(doxygen_html_dir)
        with TimedContext() as tc:
            builder = Builder(sphinx_source, sphinx_output, parallel=parallel)
            builder.build(doxygen_html_dir)
        yield tc.elapsed()


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    run_doxygen()

    sequential_timings = list(_run_and_get_timings(3, False))
    parallel_timings = list(_run_and_get_timings(3, True))

    print("\n==============")
    print("TIMING REPORT:")
    print("==============\n")

    print(f"sequential: {sequential_timings} - AVG: {sum(sequential_timings, timedelta())/len(sequential_timings)}")
    print(f"parallel: {parallel_timings} - AVG: {sum(parallel_timings, timedelta())/len(parallel_timings)}")
