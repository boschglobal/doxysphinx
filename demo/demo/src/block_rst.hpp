// =====================================================================================
// C O P Y R I G H T
// -------------------------------------------------------------------------------------
//  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
//
//  Author(s):
//  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
// =====================================================================================
#ifndef DEMO__BLOCK_RST_INCLUDED
#define DEMO__BLOCK_RST_INCLUDED

namespace doxysphinx
{
namespace doxygen
{
  /// @brief Demonstration of block rst usage. See also `:doc:"Rst Block Syntax Documentation </docs/syntax/rst_block_syntax>"`.
  ///
  class BlockRst
  {
    public:
      /// @brief RestructuredText block with markdown fences.
      ///
      ///
      /// **standard fences**
      ///
      /// *Syntax*
      /// <pre>
      /// /// ```
      /// /// {rst}
      /// /// .. tip::
      /// ///
      /// ///   If you see a tip around this text it worked!
      /// /// ```
      /// </pre>
      ///
      /// *Example*
      /// ```
      /// {rst}
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// ```
      ///
      /// **special fences**
      ///
      /// *Syntax*
      /// <pre>
      /// /// ~~~~~~~~~~~~~~~~
      /// /// {rst}
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// ~~~~~~~~~~~~~~~~
      /// </pre>
      ///
      /// *Example*
      /// ~~~~~~~~~~~~~~~~
      /// {rst}
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// ~~~~~~~~~~~~~~~~
      ///
      /// **autodetecting directives**
      ///
      /// *Syntax*
      /// <pre>
      /// /// ```
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// ```
      /// </pre>
      ///
      /// *Example*
      /// ```
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// ```
      void block_rst_via_markdown();

      /// @brief RestructuredText block doxygen verbatim special command.
      ///
      /// **verbatim command**
      ///
      /// *Syntax*
      /// <pre>
      /// /// \\verbatim {rst}
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// \\endverbatim
      /// </pre>
      ///
      /// *Example*
      /// \verbatim {rst}
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// \endverbatim
      ///
      ///
      /// **verbatim command (breathe compatibility)**
      ///
      /// *Syntax*
      /// <pre>
      /// /// \@verbatim embed:rst:leading-slashes
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// \@endverbatim
      /// </pre>
      ///
      /// *Example*
      /// \verbatim embed:rst:leading-slashes
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// \endverbatim
      ///
      ///
      /// **autodetecting directives**
      ///
      /// *Syntax*
      /// <pre>
      /// /// \\verbatim
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// \\endverbatim
      /// </pre>
      ///
      /// *Example*
      /// \verbatim
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// \endverbatim
      ///
      void block_rst_via_verbatim();

      /// @brief RestructuredText block doxygen code special command.
      ///
      /// **code command**
      ///
      /// *Syntax*
      /// <pre>
      /// /// \\code
      /// /// {rst}
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// \\endcode
      /// </pre>
      ///
      /// *Example*
      /// \code
      /// {rst}
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// \endcode
      ///
      ///
      /// **code command (breathe compatibility)**
      ///
      /// *Syntax*
      /// <pre>
      /// /// \@code embed:rst:leading-slashes
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// \@code
      /// </pre>
      ///
      /// *Example*
      /// @code embed:rst:leading-slashes
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// @endcode
      ///
      ///
      /// **autodetecting directives**
      ///
      /// *Syntax*
      /// <pre>
      /// /// \\code
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// \\endcode
      /// </pre>
      ///
      /// *Example*
      /// \code
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// \endcode
      ///
      void block_rst_via_code();

      /// @brief RestructuredText block with html pre tag in doxygen.
      ///
      /// **&lt;pre&gt;-html-element**
      ///
      /// *Syntax*
      /// <pre>
      /// /// &lt;pre&gt; {rst}
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// &lt;/pre&gt;
      /// </pre>
      ///
      /// *Example*
      /// <pre> {rst}
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// </pre>
      ///
      ///
      /// **autodetecting directives**
      ///
      /// *Syntax*
      /// <pre>
      /// /// &lt;pre&gt;
      /// /// .. tip::
      /// ///
      /// ///    If you see a tip around this text it worked!
      /// /// &lt;/pre&gt;
      /// </pre>
      ///
      /// *Example*
      /// <pre>
      /// .. tip::
      ///
      ///    If you see a tip around this text it worked!
      /// </pre>
      ///
      void block_rst_via_pre();


  }; // BlockRst

} // doxygen
} // doxysphinx

#endif
