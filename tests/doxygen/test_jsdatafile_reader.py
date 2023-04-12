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

from doxysphinx.doxygen import read_js_data_file


@pytest.fixture()
def doc_root() -> Path:
    return Path() / "docs" / "doxygen" / "demo" / "html"


def test_read_js_data_file(doc_root):
    file = doc_root / "menudata.js"
    read_js_data_file(file)
