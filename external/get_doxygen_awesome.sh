#!/bin/bash

# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================

# Script to get-doxygen-awesome (full repo, not only the css file like it's stored here at present)
echo ">>>>> cloning doxygen-awesome repo..."
VERSION=2.0.3
curl -sSL https://github.com/jothepro/doxygen-awesome-css/archive/refs/tags/v$VERSION.tar.gz | \
tar -xzvf - --strip-components=1 -C doxygen-awesome-css \
doxygen-awesome-css-$VERSION/doxygen-awesome.css \
doxygen-awesome-css-$VERSION/LICENSE

#git clone https://github.com/jothepro/doxygen-awesome-css.git
#curl -o doxygen-awesome.css https://github.com/jothepro/doxygen-awesome-css/blob/v2.0.3/doxygen-awesome.css
