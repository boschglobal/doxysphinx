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
from pyinstrument import Profiler

from doxysphinx.doxygen import DoxygenOutputPathValidator
from doxysphinx.process import Builder, Cleaner
from doxysphinx.utils.contexts import TimedContext
from doxysphinx.utils.exceptions import ApplicationError

root = Path(__file__).parent / ".."

profiler = Profiler(interval=0.01)


def _run_and_get_timings(iterations: int, doxygen_html_dir: Path, parallel: bool) -> Iterable[timedelta]:
    sphinx_source = root
    sphinx_output = root / ".build" / "html"

    for i in range(iterations):
        cleaner = Cleaner(sphinx_source, sphinx_output, parallel=parallel)
        cleaner.cleanup(doxygen_html_dir)
        with TimedContext() as tc:
            profiler.start()
            builder = Builder(sphinx_source, sphinx_output, parallel=parallel)
            builder.build(doxygen_html_dir)
            profiler.stop()
        yield tc.elapsed()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    validator = DoxygenOutputPathValidator()

    standard_demo = root / "docs" / "doxygen" / "demo" / "html"
    if not validator.validate(standard_demo):
        raise ApplicationError(f"{standard_demo} doesn't container a doxygen documentation. Please generate it first")

    graphviz_demo = root / "demo" / "graphviz" / "doxygen" / "html"
    if not validator.validate(graphviz_demo):
        raise ApplicationError(f"{graphviz_demo} doesn't container a doxygen documentation. Please generate it first")

    # sequential_timings = list(_run_and_get_timings(3, False))
    standard_demo_timings = list(_run_and_get_timings(10, standard_demo, True))
    # graphviz_demo_timings = list(_run_and_get_timings(3, graphviz_demo, True))

    print("\n==============")
    print("TIMING REPORT:")
    print("==============\n")

    # print(f"sequential: {sequential_timings} - AVG: {sum(sequential_timings, timedelta())/len(sequential_timings)}")
    print(f"demo: {standard_demo_timings} - AVG: {sum(standard_demo_timings, timedelta())/len(standard_demo_timings)}")
    # print(
    #    f"graphviz: {graphviz_demo_timings} - AVG: {sum(graphviz_demo_timings, timedelta())/len(graphviz_demo_timings)}"
    # )

    html_report = root / "bench_all_pyinstruments.html"
    html_report.write_text(profiler.output_html())
