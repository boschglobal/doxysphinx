<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Aniket Salve, Robert Bosch GmbH
=====================================================================================
-->
# Doxylink Setup

This is completely optional but we strongly recommend to install
[doxylink](https://github.com/sphinx-contrib/doxylink) for linking from sphinx documentation
directly to doxygen documented symbols like functions, classes etc.

## Setup

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

## Registration

Doxylink "knows" the c++ symbols by reading tagfiles that are generated by doxygen (this is also the reason
why tagfiles need to be enabled in doxygen config - see [](getting_started.md\#step-2-prepare-doxygen-config)).

You now need to register your doxygen documentations with in your sphinx `conf.py`
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

## Done

🎉 Congratulations you've completed the doxylink setup.

Related topics:

* To get to know the doxysphinx setup -> see our [doxysphinx guide](getting_started.md).
