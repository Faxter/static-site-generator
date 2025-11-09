import unittest

from src.node_assembler import markdown_to_html_node, text_block_to_html_node


class TestNodeAssembler(unittest.TestCase):
    def test_markdown_doc_to_html(self):
        md = markdown_to_html_node("""
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

""")
        self.assertEqual(
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            md.to_html(),
        )

    def test_markdown_doc_to_html_code_block(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
            node.to_html(),
        )

    def test_block_to_node_paragraph_plain(self):
        node = text_block_to_html_node("some plain text")
        self.assertEqual("<p>some plain text</p>", node.to_html())

    def test_block_to_node_paragraph_with_markdown(self):
        node = text_block_to_html_node("**bold** text in _here_")
        self.assertEqual(
            "<p><b>bold</b> text in <i>here</i></p>",
            node.to_html(),
        )

    def test_block_to_node_quote(self):
        node = text_block_to_html_node("> some quote")
        self.assertEqual("<blockquote>some quote</blockquote>", node.to_html())

    def test_block_to_node_quote_multiline(self):
        node = text_block_to_html_node("> some quote\n> more text")
        self.assertEqual(
            "<blockquote>some quote<br />more text</blockquote>", node.to_html()
        )

    def test_block_to_node_ulist(self):
        node = text_block_to_html_node("- item 1\n- item 2")
        self.assertEqual("<ul><li>item 1</li><li>item 2</li></ul>", node.to_html())

    def test_block_to_node_olist(self):
        node = text_block_to_html_node("1. item 1\n2. item 2")
        self.assertEqual("<ol><li>item 1</li><li>item 2</li></ol>", node.to_html())

    def test_block_to_node_code(self):
        node = text_block_to_html_node(
            "```This is text that _should_ remain\nthe **same** even with inline stuff\n```"
        )
        self.assertEqual(
            "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre>",
            node.to_html(),
        )

    def test_block_to_node_heading(self):
        node = text_block_to_html_node("# heading 1")
        self.assertEqual("<h1>heading 1</h1>", node.to_html())

    def test_block_to_node_heading6(self):
        node = text_block_to_html_node("###### heading 6")
        self.assertEqual("<h6>heading 6</h6>", node.to_html())
