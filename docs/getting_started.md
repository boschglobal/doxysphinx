<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->
# Getting Started

Welcome to doxysphinx. In this guide we'll walk you through setting up doxysphinx for your doxygen and sphinx
project.

> This guide expects that you want to integrate doxysphinx in your own project. If you just want to testdrive
> it and see how things working we recommend to clone the repo, fire up vscode and enter the devcontainer.

## Step 0: Prerequisites

Please be sure to fulfill the following prerequisites.

```{hint}
You can also look at the source code of this project for reference - especially the
[devcontainer](https://todo_link_latest_devcontainer_here) here everything is set up.
```

### Project requirements

You need a project upfront with:

* doxygen installed and configured.
* sphinx installed and configured.

### Needed tooling

You should already have installed python, doxygen and sphinx. If yes - great! If not please install them:

* [Python 3.7+](https://www.python.org)
* [Doxygen](https://doxygen.nl)
* [Sphinx](https://www.sphinx-doc.org)
* [DartSass](https://sass-lang.com/dart-sass)

  ``````{card} DartSass installation
  :margin: 1
  `````{tab-set}
  ````{tab-item} Linux
  ```bash
  # Linux
  curl -sSL https://github.com/sass/dart-sass/releases/download/1.49.7/dart-sass-1.49.7-linux-x64.tar.gz | tar -xzvf - --strip-components=1 -C ~/.local/bin dart-sass/sass
  ```
  ````
  ````{tab-item} Windows
  ```powershell
  # windows with chocolatey (https://www.chocolatey.org)
  choco install sass
  ```
  ````
  ````{tab-item} Other
  see Releases: <https://github.com/sass/dart-sass/releases>.
  ````
  `````
  ``````

## Step 1: Installing Doxysphinx

Doxysphinx is distributed as [pypi package](https://todo_add_link_here).

Install it with:

```shell
pip install doxysphinx
```

```{note}
If you have trouble installing/running the package, please look into our [FAQ](faq.md#I.1) where we describe
some alternatives.
```

## Step 2: Install and setup Doxylink

This is completely optional but we strongly recommend to install
[doxylink](https://github.com/sphinx-contrib/doxylink) for linking from sphinx documentation
directly to Doxygen documented symbols like functions, classes etc.

### Setup

Install pip package:

```shell
pip install sphinxcontrib-doxylink
```

Activate the doxylink extension in your sphinx `conf.py`:

```python
extensions = [
  # all the other extension
  "sphinxcontrib.doxylink",
]
```

### Registration

Now you need to register your doxygen documentations with in your sphinx `conf.py`
with doxylink with the `doxylink` variable:

```python
doxygen_root = "docs/doxygen" # this is just a convenience variable
doxylink = {
    "demo": (  # "demo" is the role name that you can later use in sphinx to reference this doxygen documentation (see below)
        f"{doxygen_root}/demo/html/tagfile.xml", # the first parameter of this tuple is the tagfile
        f"{doxygen_root}/demo/html", # the second parameter of this tuple is a relative path pointing from
                                     # sphinx output directory to the doxygen output folder inside the output
                                     # directory tree.
                                     # Doxylink will use the tagfile to get the html file name of the symbol you want
                                     # to link and then prefix it with this path to generate html links (<a>-tags).
    ),
}
```

Register all your doxygen documentions via this mechanism.
In your rst files you can then use e.g. (as documented here: <https://sphinxcontrib-doxylink.readthedocs.io/en/stable/>)

```rst
The class :demo:`doxysphinx::rst::Car` implements the car.
```

## Step 3: Prepare Doxygen Config

Next you have to prepare your doxygen configuration file (doxyfile) to have compatible settings with doxysphinx.

The following settings are mandatory:

You can prepare or optimize your doxygen configuration file (doxyfile) by doing the following:

### Mandatory settings

these settings are absolutely needed:

```yaml
OUTPUT_DIRECTORY       = <anywhere_below_you_sphinx_documentation_source_root!!!> # see note below

SEARCHENGINE           = NO   # Deactivate search engine (as sphinx has it's own search)
GENERATE_TREEVIEW      = NO   # Deactivate doxygens own treeview (as it doesn't look right)
DISABLE_INDEX          = NO   # Menu data is crucial for our TOC generation so it mustn't be disabled

GENERATE_HTML          = YES  # Keep sure that you generate HTML which needed for doxysphinx
ALIASES                = "rst=\verbatim embed:rst:leading-asterisk" \
                         endrst=\endverbatim  # This allows you to use rst blocks inside doxygen comments with @rst and @endrst
GENERATE_TAGFILE       = <OUTPUT_DIRECTORY>/<HTML_OUTPUT>/tagfile.xml  # generate a tag file
                              # this could be stored anywhere, however we recommend to put it into the
                              # documentation output folder which is the value of the OUTPUT_DIRECTORY variable
                              # + the value of the HTML_OUTPUT variable (your have to expand it for yourself
                              # because doxygen has no mechanism to reference config settings that were defined
                              # beforehand.
                              # The tagfile is also needed for the doxylink extension

CREATE_SUBDIRS         = NO   # NO is the default value and it should be no because doxysphinx can't handle subdirs right now.
```

```{note}
_Why the heck the doxygen output_dir needs to live inside the sphinx docs root?_

Right now for each doxygen html output file a rst file is generated with the same name/path but different extension.
We did this because sphinx will then automatically generate the html files for the rsts at the correct relative location -
and no doxygen-documentation-internal links will break - they just stay the same. However this has the implication that
the doxygen html output has to live inside/somewhere below the sphinx source directory (we recommend using something
like `docs/doxygen/YOUR_LIBRARY_NAME/`). If that isn't the case for you doxysphinx will complain and exit.

_But I don't want my docs dir to get polluted with generated code!_

Yes, we don't like that either, but one of our design goals was performance and scanning htmls and correcting links
is just one additional step that takes time and makes things more complicated.

Our recommendation is to just gitignore the generated doxygen docs dir. If you cannot live with it you could take a
look at the [alternatives](./alternatives.md).
```

### Recommended settings

these settings are optional but strongly recommended:

```yaml
GENERATE_XML           = NO   # Xml output isn't needed for doxysphinx

DOT_IMAGE_FORMAT       = svg  # generates nicer svg images
DOT_TRANSPARENT        = YES  # generate transparent images
INTERACTIVE_SVG        = YES  # to be able to scroll and zoom into big images

# doxygen awesome
# ===============
# doxygen awesome <https://jothepro.github.io/doxygen-awesome-css/> is a stylesheet that makes doxygen documentation look beautiful.
# We strongly recommend using it # because then the doxygen docs would fit far better with any sphinx theme.
# Just download/clone the doxygen awesome stylesheet and then add it to your doxygen config:

HTML_EXTRA_STYLESHEET = YOUR_DOXYGEN_AWESOME_PATH/doxygen-awesome.css
```

## Step 4: Run Doxysphinx

Now it's time to run doxysphinx.

You can either do it manually or integrate it in your makefile, cmake, whatever...

### Manually

```{note}
Keep sure that you first run doxygen.
```

The doxysphinx cli/executable has the following commands/options.

#### Get help

Show command and usage information. This will also show the most up to date documentation as this guide will
only handle the basics:

```bash
doxysphinx --help
doxysphinx <command> --help
```

### Build

Build the sphinx rst documents out of the doxygen htmls.

```bash
doxysphinx build <SPHINX_SOURCE> <SPHINX_OUTPUT> <DOXYFILE(S)>
```

Arguments:

| Variable       | Descriptions                                                                                                                                                                |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SPHINX_SOURCE  | The root of your sphinx source/input directory tree.<br/>Often this is the same directory your conf.py is in.                                                               |
| SPHINX_OUTPUT  | The root of you sphinx output directory tree - where sphinx puts the generated html files to.<br/> This should be the directory where sphinx put's it's main index.html to. |
| DOXYFILE(S)    | One or many doxygen configuration files that all should stick to the setting recommendation from [STEP-3](#step-3)                                                          |

Replace the following arguments:

```{warning}
Please note that sphinx has slightly different output directories depending on the arguments:
* <pre>sphinx-build <strong>-b</strong> html SOURCE_DIR OUTPUT_DIR ...</pre>
  the html output will be put to `OUTPUT_DIR` so doxysphinx's `SPHINX_OUTPUT` should be `OUTPUT_DIR`.
* <pre>sphinx-build <strong>-M</strong> html SOURCE_DIR OUTPUT_DIR ...</pre>
  the html output will be put to `OUTPUT_DIR/html` so doxysphinx's `SPHINX_OUTPUT` should be `OUTPUT_DIR/html`.
```

### Clean

If you want to clean the files doxysphinx generated please use the clean command:

```bash
doxysphinx clean <SPHINX_SOURCE> <SPHINX_OUTPUT> <DOXYFILE(S)>
```

### Makefile integration

Add/extend the following targets in your makefile:

```makefile
clean:
  @doxysphinx clean <SPHINX_SOURCE> <SPHINX_OUTPUT> <DOXYFILE(S)>

doxysphinx:
  @doxysphinx build <SPHINX_SOURCE> <SPHINX_OUTPUT> <DOXYFILE(S)>
```

Now you just need to call the doxysphinx target __right after your doxygen is running__.

### Step 5: Use rst snippets in your C/C++ Sourcecode

Finally we can start using rst snippets in doxygen comments.

Open some C/C++ file and add a comment like this to one of your functions/methods/whatever:

```cpp
/// @brief Creates a new instance of the Car.
///
/// @param engine - the engine to use for this Car.
/// @param color - the color of this Car.
///
/// @rst
/// .. hint::
///    Rst text can also be included after the params.
///
/// @endrst
Car(Engine& engine, Color& color) {};
```

Note the `@rst` and `@endrst` tags. Inside these tags you can write any rst code.
Now run doxygen, doxysphinx and sphinx and look at the generated documentation. You should see something like
this:

```{image} resources/getting_started_demo_rendering.png
:alt: Demo of final generated html
:width: 900px
```

## Done

|:tada:| Congratulations you've completed the quickstart.

Further reading:

* Maybe you want to know more about the inner workings? -> head over to the reference section.
* Or look at some examples? -> examples.
* Or do you want to contribute and bring doxysphinx to the next level? Read the contributors guide and the
  Developers section.

Or just start documenting {material-twotone}`sentiment_satisfied;2em`.
