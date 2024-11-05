doxysphinx.html_parser
======================

.. py:module:: doxysphinx.html_parser

.. autoapi-nested-parse::

   The html_parser module contains the html parser that will load and process the html files.

   To allow several :mod:`writer` implementations to pick up and handle the result of that parsing a html parser
   in a neutral way the parser will change all relevant rst/sphinx markup elements to `<snippet>`-elements.



Classes
-------

.. autoapisummary::

   doxysphinx.html_parser.HtmlParseResult
   doxysphinx.html_parser.HtmlParser
   doxysphinx.html_parser.ElementProcessor
   doxysphinx.html_parser.RstInlineProcessor
   doxysphinx.html_parser.RstBlockProcessor
   doxysphinx.html_parser.PreToDivProcessor
   doxysphinx.html_parser.MarkdownRstBlockProcessor
   doxysphinx.html_parser.DoxygenHtmlParser


Module Contents
---------------

.. py:class:: HtmlParseResult

   Capsules a parsed and processed html tree with meta information.


   .. py:attribute:: html_input_file
      :type:  pathlib.Path

      The html file that was parsed.


   .. py:attribute:: project
      :type:  str

      The project where this html file belongs to.
      This can be e.g. a directory name or a component/module name etc.


   .. py:attribute:: meta_title
      :type:  str

      The html meta title if present in the original html.
      If not just set to document title


   .. py:attribute:: document_title
      :type:  str

      The document title. This is the title that is visible e.g.
      in sphinx menu structure.


   .. py:attribute:: used_snippet_formats
      :type:  Optional[Set[str]]

      The list of snippet formats that are used inside the html tree if any.


   .. py:attribute:: tree
      :type:  Optional[lxml.etree._ElementTree]

      The html/xml element tree or None if nothing was parsed because the html shouldn't be handled as mixed
      mode content.


.. py:class:: HtmlParser(source_directory: pathlib.Path)

   Bases: :py:obj:`Protocol`

   .. autoapi-inheritance-diagram:: doxysphinx.html_parser.HtmlParser
      :parts: 1


   Html Parser Protocol for parsing html files into a neutral format (that can be then processed further).

   You own html parser should find/generate all rst-content in <rst>-tags.
   The further tooling can then work with that.


   .. py:method:: parse(file: pathlib.Path) -> HtmlParseResult
      :abstractmethod:


      Parse a html file.

      This method returns a ParseResult (Tuple[bool, _ElementTree]).
      The first item in the tuple indicates if rst data was found during parsing.
      The second item is the parsed and normalized html as ElementTree.
      It is expected that all rst data in this resulting ElementTree is present in special
      <rst>-tags.

      :param file: The html file to parse
      :return: The result of the parsing



.. py:class:: ElementProcessor

   Bases: :py:obj:`Protocol`

   .. autoapi-inheritance-diagram:: doxysphinx.html_parser.ElementProcessor
      :parts: 1


   An ElementProcessor processes specific html elements, one at a time.

   Typically this is used to either clean up or transform the elements into a neutralized format.


   .. py:attribute:: elements
      :type:  List[str]
      :value: []


      A list of html element names this processor can process.

      This is for pre-filtering html elements (an optimization). This processors try_process method
      is only called on these elements.


   .. py:attribute:: is_final
      :type:  bool
      :value: True


      Whether other processors should be called after this one.

      With a "final processor" (is_final == True) processing of an element stops (no other processors considered)
      once the try_process method returns True.


   .. py:attribute:: format
      :type:  str
      :value: 'None'


      The format this element processor processes... like 'rst', 'md' etc.


   .. py:method:: try_process(element: lxml.etree._Element) -> bool

      Try to process an element.

      :param element: The element to check and process
      :return: Whether the "processor did it's thing"/"processing was applied" (True) or not (False)



.. py:class:: RstInlineProcessor

   Element Processor for inline rst elements.


   .. py:attribute:: elements
      :value: ['code']



   .. py:attribute:: format
      :value: 'rst'



   .. py:attribute:: is_final
      :value: True



   .. py:attribute:: rst_role_regex


   .. py:method:: try_process(element: lxml.etree._Element) -> bool

      Try to process an rst inline element into a neutralized format.

      :param element: The html element to process
      :return: True if the element was processed else False



.. py:class:: RstBlockProcessor

   Element Processor for rst block elements.


   .. py:attribute:: elements
      :value: ['code', 'pre']



   .. py:attribute:: format
      :value: 'rst'



   .. py:attribute:: is_final
      :value: True



   .. py:method:: try_process(element: lxml.etree._Element) -> bool

      Try to process an rst block element into a neutralized format.

      :param element: The html element to process
      :return: True if the element was processed else False



.. py:class:: PreToDivProcessor

   This Element Processor will change <pre>-tags to <div class="fragments"> tags.

   We do this because doxysphinx will linearize html output in the writer to have it in one line in
   the raw html directive. However this will destroy the newlines in pre tags. To overcome that
   We change the pre output here to a div with inner line divs (which is also supported by doxygen).

   This processor is special because it should only run when any other processor has done something.


   .. py:attribute:: elements
      :value: ['pre']



   .. py:attribute:: format
      :value: ''



   .. py:attribute:: is_final
      :value: True



   .. py:method:: try_process(element: lxml.etree._Element) -> bool

      Transform a pre element into a div element.

      :param element: The html element to process
      :return: True if the element was processed else False



.. py:class:: MarkdownRstBlockProcessor

   Element Processor for doxygen markdown block elements.

   This processor will check if the first line in the markdown block is either a supported marker or
   a directive (auto detection feature).

   Markdown block elements in doxygen are getting rendered different to verbatim content.
   Each Markdown block (delimited with 3 backticks) will be something like this in html:

   .. code-block:: html

      <div class="fragment">
        <div class="line">{rst}</div>
        <div class="line">This is rst content</div>
        <div class="line"> </div>
        <div class="line">anything can be used here...</div>
        <div class="line"> </div>
        <div class="line">like an admonition:</div>
        <div class="line"> </div>
        <div class="line">..admonition::</div>
        <div class="line">  </div>
        <div class="line">  test</div>
      </div>


   .. py:attribute:: elements
      :value: ['div']



   .. py:attribute:: format
      :value: 'rst'



   .. py:attribute:: is_final
      :value: True



   .. py:method:: try_process(element: lxml.etree._Element) -> bool

      Try to process an rst block element into a neutralized format.

      :param element: The html element to process
      :return: True if the element was processed else False



.. py:class:: DoxygenHtmlParser(source_directory: pathlib.Path)

   Parser for Doxygen HTML output files.


   .. py:method:: parse(file: pathlib.Path) -> HtmlParseResult

      Parse a doxygen HTML file into an ElementTree and normalize its inner data to contain <rst>-tags.

      :param file: The html file to parse
      :type file: Path
      :return: The result of the parsing
      :rtype: ParseResult



