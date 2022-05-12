#!/bin/bash

# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

# Script to get-doxygen-awesome (full repo, not only the css file like it's stored here at present)
echo ">>>>> cloning doxygen-awesome repo..."
git clone https://github.com/jothepro/doxygen-awesome-css --depth=1
rm -rf doxygen-awesome-css/.git
