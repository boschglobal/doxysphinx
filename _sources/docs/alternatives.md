<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
 - Nirmal Sasidharan, Robert Bosch Gmbh
=====================================================================================
-->
# Alternatives

If doxysphinx doesn't fit your needs maybe there are some other open source tools which might be a better fit:

* [Breathe](https://github.com/michaeljones/breathe)
* [Exhale](https://github.com/svenevs/exhale)
* [Doxyrest](https://github.com/vovkos/doxyrest)
* [wurfapi](https://github.com/steinwurf/wurfapi)
* [sphinxcontrib-autodoc_doxygen](https://github.com/rmcgibbo/sphinxcontrib-autodoc_doxygen)

These seem abandoned:

* [gasp](https://github.com/troelsfr/Gasp)
* [doxygraph](https://github.com/jitsuCM/doxygraph)

## Doxysphinx vs Breathe vs Exhale

The tools [Breathe](https://breathe.readthedocs.io/en/latest/) and [Exhale](https://exhale.readthedocs.io/en/latest/index.html) needs special mention, as doxysphinx was invented in a large C++ project (> 11,000 C++ files) where we started out with these two tools. With the large project size, Exhale did not perform too well and Breathe did not quite support all C++ and Doxygen features that C++ developers expected. Doxysphinx was invented to overcome these limitations.

Breathe is useful for smaller C++ projects when parts of C++ Doxygen documentation needs to be integrated into the Sphinx documentation using [Breathe directives](https://breathe.readthedocs.io/en/latest/directives.html).
When the complete C++ Doxygen documentation needs to be integrated into Sphinx, the following options are available:

* [breathe.apidoc](https://github.com/michaeljones/breathe/blob/master/breathe/apidoc.py)
* [Exhale](https://exhale.readthedocs.io/en/latest/index.html)

Doxysphinx outperforms the two options w.r.t to speed and features, as it simply reuses Doxygen output.

Also note that Breathe and Doxysphinx can co-exist in the same project.
