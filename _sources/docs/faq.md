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

(faq-i-1)=

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

Head over to the [github releases]({{ repo }}/releases) section and download the pex package.
This is a self contained executable which should work if you have a compatible python installed.

## Styling/Customizing

### S.1 - Element X looks ugly with my theme Y. How can I change that?

You can try to override the CSS styles for your theme.
If you take a look into our repo's [`docs/_static`]({{ code }}/docs/_static/) folder you can see 2 custom theme-override-css files.
The mechanism to load the correct one is defined in the [`conf.py`]({{ code }}/conf.py) (`html_css_files` setting).

However in general you just need to put your css into a path configured in `html_static_path` and then reference
it in `html_css_files` and it will get loaded.

## Contribution

### C.1 - Some of the graphics in here are sketch files, how can i use them?

We use [Lunacy](https://icons8.com/lunacy) at present as graphics editor to just get svg files in the end.
At present Lunacy is free for personal and commercial use.

The sketch format can also be used with [Sketch](https://www.sketch.com/) and other tools like
[Figma](https://www.figma.com) are also able to at least import it.

However in the end any svg editor will do. If you contribute, contribute svgs. If you're happening to use
another editing tool that has another native format you can just check the original sources in.

If you want to stay full open source [Inkscape](https://inkscape.org) is a very good option to just have a
good svg editor.

### C.2 - Which image format should i use for documentation?

In descending order of preference:

* svg
* png

If these formats cuts information from the original file please also consider providing the original.
