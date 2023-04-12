# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

from pathlib import Path

from doxysphinx.utils.files import write_file


def test_writefile(tmp_path):

    file: Path = tmp_path / "test.txt"
    content = ["This", "is", "a", "test", "file"]
    write_file(file, content)

    result = file.read_text()
    content.append("")  # because we write a trailing newline in every case but join won't add it.
    assert "\n".join(content) == result
