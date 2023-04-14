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

from doxysphinx.toc import DoxygenTocGenerator


def test_tocgenerator_works_as_expected():
    tocgen = DoxygenTocGenerator(Path(__file__).parent)
    path = Path("index.html")
    result = list(tocgen.generate_toc_for(path))
    assert result[0] == ".. toctree::"
    assert result[5] == "   Modules <modules>"
    assert result[7] == "   Files <files_files>"
    assert result[8] == "   Illegal/#^ chárs <a_illegal__chars>"
