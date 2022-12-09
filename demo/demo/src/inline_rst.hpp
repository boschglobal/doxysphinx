// =====================================================================================
// C O P Y R I G H T
// -------------------------------------------------------------------------------------
//  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
//
//  Author(s):
//  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
// =====================================================================================
#ifndef DEMO__INLINE_RST_INCLUDED
#define DEMO__INLINE_RST_INCLUDED

namespace doxysphinx
{
namespace doxygen
{
  /// @brief Demonstration of inline rst usage. See also `:doc:"Rst Inline Syntax Documentation </docs/syntax/rst_inline_syntax>"`.
  class InlineRst
  {
    public:
      /// @brief shows how to use inline rst roles in doxygen comments
      ///
      /// #### syntax
      /// use this syntax in your doxygen comments (we left out the comment prefix [///, //! etc.] here).
      ///
      /// ```plain
      /// 1) A html code element with quotes like this - <code>:doc:"This is an inline link to the Main Documentation <index>"</code> - should work.
      ///
      /// 2) A html code element with ticks like this - <code>:doc:'This is an inline link to the Main Documentation <index>'</code> - should work.
      ///
      /// 3) A html code element with escaped backticks like this - <code>:doc:\`This is an inline link to the Main Documentation <index>\`</code> - should work.
      ///
      /// 4) A tt element with quotes like this - <tt>:doc:"This is an inline link to the Main Documentation <index>"</tt> - should work.
      ///
      /// 5) A tt element with ticks like this - <tt>:doc:'This is an inline link to the Main Documentation <index>'</tt> - should work.
      ///
      /// 6) A tt element with escaped backticks like this - <tt>:doc:\`This is an inline link to the Main Documentation <index>\`</tt> - should work.
      ///
      /// 7) A markdown inline statement with quotes like this - `:doc:"This is an inline link to the Main Documentation <index>"` - should work.
      ///
      /// <em>Not working</em>:
      ///
      /// 8!) A markdown inline statement with ticks like this - `:doc:'This is an inline link to the Main Documentation <index>'` - won't work because
      ///     doxygen generates <code>&lsquo;</code> and <code>&rsquo;</code> symbols instead of \em code-tags in this case (which is strange btw...).
      ///
      /// 9!) Escaping backticks in markdown inline statement - `:doc:\`This is an inline link to the Main Documentation <index>\`` - won't work because
      ///     doxygen preprocesses that in a strange way.
      /// ```
      ///
      /// #### visual example
      ///
      /// 1) A html code element with quotes like this - <code>:doc:"This is an inline link to the Main Documentation <index>"</code> - should work.
      ///
      /// 2) A html code element with ticks like this - <code>:doc:'This is an inline link to the Main Documentation <index>'</code> - should work.
      ///
      /// 3) A html code element with escaped backticks like this - <code>:doc:\`This is an inline link to the Main Documentation <index>\`</code> - should work.
      ///
      /// 4) A tt element with quotes like this - <tt>:doc:"This is an inline link to the Main Documentation <index>"</tt> - should work.
      ///
      /// 5) A tt element with ticks like this - <tt>:doc:'This is an inline link to the Main Documentation <index>'</tt> - should work.
      ///
      /// 6) A tt element with escaped backticks like this - <tt>:doc:\`This is an inline link to the Main Documentation <index>\`</tt> - should work.
      ///
      /// 7) A markdown inline statement with quotes like this - `:doc:"This is an inline link to the Main Documentation <index>"` - should work.
      ///
      /// <em>Not working</em>
      ///
      /// 8!) A markdown inline statement with ticks like this - `:doc:'This is an inline link to the Main Documentation <index>'` - won't work because
      ///     doxygen generates <code>&lsquo;</code> and <code>&rsquo;</code> symbols instead of \em code-tags in this case (which is strange btw...).
      ///
      /// 9!) Escaping backticks in markdown inline statement - `:doc:\`This is an inline link to the Main Documentation <index>\`` - won't work because
      ///     doxygen preprocesses that in a strange way.
      void inline_rst_syntax_in_comments();

      /// @brief shows how to use inline rst roles in doxygen list comments
      ///
      /// #### syntax
      /// use this syntax in your doxygen comments (we left out the comment prefix [///, //! etc.] here).
      ///
      /// ```plain
      /// 1. A html code element with quotes like this - <code>:doc:"This is an inline link to the Main Documentation <index>"</code> - should work.
      /// 2. A html code element with ticks like this - <code>:doc:'This is an inline link to the Main Documentation <index>"</code> - should work.
      /// 3. A html code element with escaped backticks like this - <code>:doc:\`This is an inline link to the Main Documentation <index>\`</code> - should work.
      /// 4. A tt element with quotes like this - <tt>:doc:"This is an inline link to the Main Documentation <index>"</tt> - should work.
      /// 5. A tt element with ticks like this - <tt>:doc:'This is an inline link to the Main Documentation <index>'</tt> - should work.
      /// 6. A tt element with escaped backticks like this - <tt>:doc:\`This is an inline link to the Main Documentation <index>\`</tt> - should work.
      /// 7. A markdown inline statement with quotes like this - `:doc:"This is an inline link to the Main Documentation <index>"` - should work.
      /// ```
      ///
      /// #### visual example
      ///
      /// 1. A html code element with quotes like this - <code>:doc:"This is an inline link to the Main Documentation <index>"</code> - should work.
      /// 2. A html code element with ticks like this - <code>:doc:'This is an inline link to the Main Documentation <index>'</code> - should work.
      /// 3. A html code element with escaped backticks like this - <code>:doc:\`This is an inline link to the Main Documentation <index>\`</code> - should work.
      /// 4. A tt element with quotes like this - <tt>:doc:"This is an inline link to the Main Documentation <index>"</tt> - should work.
      /// 5. A tt element with ticks like this - <tt>:doc:'This is an inline link to the Main Documentation <index>'</tt> - should work.
      /// 6. A tt element with escaped backticks like this - <tt>:doc:\`This is an inline link to the Main Documentation <index>\`</tt> - should work.
      /// 7. A markdown inline statement with quotes like this - `:doc:"This is an inline link to the Main Documentation <index>"` - should work.
      void inline_rst_syntax_in_lists();

      /// @brief shows how to use inline rst roles in doxygen list comments
      ///
      /// #### syntax
      /// use this syntax in your doxygen comments (we left out the comment prefix [///, //! etc.] here).
      ///
      /// ```plain
      /// markdown table:
      ///
      /// First Header  | Second Header
      /// ------------- | -----------------------------------
      /// Content Cell  | `:doc:"Main Documentation <index>"`
      /// Content Cell  | Content Cell
      ///
      /// html table:
      /// <table>
      /// <tr><th>First Header</th><th>Second Header></th></tr>
      /// <tr><td>Content Cell</td><td>`:doc:"Main Documentation <index>"`</td></tr>
      /// <tr><td>Content Cell</td><td>Content Cell</td></tr>
      /// </table>
      /// ```
      ///
      /// #### visual example
      ///
      /// markdown table:
      ///
      /// First Header  | Second Header
      /// ------------- | -----------------------------------
      /// Content Cell  | `:doc:"Main Documentation <index>"`
      /// Content Cell  | Content Cell
      ///
      /// html table:
      /// <table>
      /// <tr><th>First Header</th><th>Second Header</th></tr>
      /// <tr><td>Content Cell</td><td>`:doc:"Main Documentation <index>"`</td></tr>
      /// <tr><td>Content Cell</td><td>Content Cell</td></tr>
      /// </table>
      void inline_rst_syntax_in_tables();

  }; // InlineRst

} // doxygen
} // doxysphinx

#endif
