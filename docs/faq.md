<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->
# FAQ

## Installation

### I.1 - I cannot install doxysphinx because of dependency clashes with my existing environment

Doxysphinx doesn't have many runtime dependencies, however especially click (cli tool) might introduce
these problems (as it's very widely used).

You have several options:

#### 1. Use a virtual environment

First time setup:

```shell
# create a new virtual environment in your project root
python3 -m venv .venv-doxysphinx

# install doxysphinx into new virtual environment
.venv-doxysphinx/bin/pip3 installdoxysphinx
```

Usage:

```shell
# you then have 2 options to call doxysphinx:

# Option A): call doxysphinx inside virtualenv
source .venv-doxysphinx/bin/activate
doxysphinx

# Option B): call doxysphinx directly without activating venv
.venv-doxysphinx/bin/doxysphinx
```

#### 2. Use the pex package

Head over to the github releases section and download the pex package.
This is a self contained executable which should work if you have a compatible python installed.

## Styling/Customizing

### S.1 - Element X looks ugly with my theme Y. How can I change that?

You can try to override the CSS styles for your theme.
If you take a look into our repo's [](docs/_static/) folder you can see 2 custom theme-override-css files.
The mechanism to load the correct one is defined in the [](../conf.py) (`html_css_files` setting).

However in general you just need to put your css into a path configured in `html_static_path` and then reference
it in `html_css_files` and it will get loaded.

## Misc

### M.1 - Why this logo?

Mhmm, ok not that creative... a sphinx that dreams about C++...
