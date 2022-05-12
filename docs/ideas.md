<!--
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
=====================================================================================
-->
# Improvement Ideas

This is not a roadmap but some ideadump as input for a future roadmap...

* `[Feature]` Implement myst-markdown support for doxygen documentation. As doxygen itself has markdown support this
   might bring a tighter integration syntax-wise.
* `[Performance, dev]` Implement pytest-xdist to have parallel text execution
* `[Architecture]` Make doxysphinx more generic - rename to something like "Sphinx HTML Integrator (sphi)"
   (perhaps then use the greek phi character in logo ;-)). This would mean to implement something like a processor-layer
   where each processor (e.g. "doxygen", "ea", "word", "confluence" etc.) implements rst generation for a special kind
   of input html format.
* `[Performance, Dev]` Test replacing poetry (which is slow at time) with
   [pyflow](https://github.com/David-OConnor/pyflow). Note that [PDM](https://pdm.fming.dev/) was tested before.
   At the beginning it looked promising/better than poetry but we didn't manage to adapt the developer tools cleanly
   to it (pylance, pytest etc.).
* `[Improvement]` Investigate patching / cleaning up doxygen html to prevent multiple css hacks
* `[Feature]` Automatically setup doxylink for all referenced doxygen documentations
* `[Feature]` Create runtime docker container that has all necessary dependencies set up.
