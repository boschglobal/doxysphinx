doxysphinx.resources
====================

.. py:module:: doxysphinx.resources

.. autoapi-nested-parse::

   The resources module contains classes will do resource provisioning and patching.

   Resources are stylesheets, images, javascripts etc. that contemplate the html files.



Classes
-------

.. autoapisummary::

   doxysphinx.resources.ResourceProvider
   doxysphinx.resources.DoxygenResourceProvider
   doxysphinx.resources.CssScoper


Module Contents
---------------

.. py:class:: ResourceProvider(directory_mapper: doxysphinx.sphinx.DirectoryMapper)

   Bases: :py:obj:`Protocol`

   .. autoapi-inheritance-diagram:: doxysphinx.resources.ResourceProvider
      :parts: 1


   A resource provider copies/adapts necessary resources (images, stylesheets, etc.) to output.


   .. py:method:: provide_resources(resource_root: pathlib.Path) -> List[pathlib.Path]

      Provide necessary resources to sphinx output directory.

      Can also do postprocessing etc.

      :param resource_root: the root resource input directory (e.g. where the html
          files are located)
      :return: A list of resources (their target paths) that were copied/provided.
          Note that in case of some caching (copy if newer) mechanisms this might
          return only parts of the resources.



   .. py:method:: cleanup_resources(resource_root: pathlib.Path) -> List[pathlib.Path]

      Clean up provided resources that were copied by :meth:`provide_resources`.

      :param resource_root: the root resource input directory (e.g. where the html
          files are located)
      :return: A list of resources (their target paths) that were cleaned up/removed.



.. py:class:: DoxygenResourceProvider(directory_mapper: doxysphinx.sphinx.DirectoryMapper)

   Resource provider that will copy/adapt doxygen html resources to output.

   Resource are e.g. stylesheets, images, javascript files etc.


   .. py:method:: provide_resources(resource_root: pathlib.Path) -> List[pathlib.Path]

      Copy doxygen html resource files (see GLOB_PATTERN below) to sphinx output.

      The content in the raw html directives can then access these directly.

      :type resource_root: the root of the resources (= usually the same folder where
          the html file are located).



   .. py:method:: cleanup_resources(resource_root: pathlib.Path) -> List[pathlib.Path]

      Clean up any provisioned resources that were copied to sphinx output.



.. py:class:: CssScoper(css_selector: str)

   Scopes css-stylesheets to a special selector.

   This is done with the help of libsass (as the sass-syntax extends css with nesting).

   Our original problem was that the doxygen stylesheet and the sphinx theme stylesheets collide in some
   ways (e.g. global styles like heading-styles etc...). We therefore needed to have a mechanism to apply
   doxygen stylesheets only to doxygen content (not to the outer sphinx theme shell). We do this via sass,
   because sass is css compatible but adds some nice features to it. You can for example nest styles.
   We use that here to define an outer class and nest the whole doxygen stylesheet below it in a temporary
   sass stylesheet which then gets compiled back to css. With this
   we kill 2 birds with one stone:
   * all doxygen rules are now scoped so they are not applied to the sphinx bits shell anymore....
   * all doxygen rules now are more specialized than any of the outer sphinx style rules (they will win in browser).

   In the end that means that sphinx styles are applied to sphinx bits and doxygen styles are applied to
   doxygen bits. We still need to fix some minor issues with a custom stylesheet (which we also apply here).


   .. py:method:: scope(stylesheet: pathlib.Path, target: pathlib.Path, additional_css_rules: Optional[str] = None, content_patch_callback: Optional[Callable[[str], str]] = None) -> Optional[pathlib.Path]

      Scope a stylesheet to given selector.

      The process is as follows: The original stylesheet is read, processed, hashed and compiled to the
      target. If a target already exists and the hash is identical nothing is compiled and written.

      :param stylesheet: The path to a stylesheet to scope.
      :param: target: The path to a stylesheet where the results are written to.
      :param additional_css_rules: Additional css rules to inject.
      :param scss_patch_callback: A callback that will be called on the original file.
             Note: we had a bug in doxygen.css and a sass compatibility fix for doxygen-awesome that made
             this mechanism necessary. With one of the recent doxygen versions the doxygen.css bug was fixed
             however we still keep it here some time.
      :return: The path to the written stylesheet (should be identical to stylesheet).



