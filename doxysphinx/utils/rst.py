# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The rst module contains rst specific helpers."""

_rst_safe_encode_map = str.maketrans(
    {
        "_": r"\_",
        "\\": r"\\",
        "^": r"\^",
        "$": r"\$",
        "*": r"\*",
        "`": r"\`",
    }
)


def rst_safe_encode(text: str) -> str:
    """Encode text to be rst safe (special chars will get escaped correctly).

    :param text: The text to encode.
    :return: The rst safe encoded text
    """
    return text.translate(_rst_safe_encode_map)
