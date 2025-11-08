import unittest

from src.node_assembler import text_block_to_html_node


class TestNodeAssembler(unittest.TestCase):
    def test_block_to_node_paragraph_plain(self):
        node = text_block_to_html_node("some plain text")
        self.assertEqual("<div><p>some plain text</p></div>", node.to_html())

    def test_block_to_node_paragraph_with_markdown(self):
        node = text_block_to_html_node("**bold** text in _here_")
        self.assertEqual(
            "<div><p><b>bold</b> text in <i>here</i></p></div>",
            node.to_html(),
        )

    def test_block_to_node_quote(self):
        node = text_block_to_html_node("> some quote")
        self.assertEqual(
            "<div><blockquote>some quote</blockquote></div>", node.to_html()
        )

    def test_block_to_node_quote_multiline(self):
        node = text_block_to_html_node("> some quote\n> more text")
        self.assertEqual(
            "<div><blockquote>some quote more text</blockquote></div>", node.to_html()
        )

    def test_block_to_node_ulist(self):
        node = text_block_to_html_node("- item 1\n- item 2")
        self.assertEqual(
            "<div><ul><li>item 1</li><li>item 2</li></ul></div>", node.to_html()
        )

    def test_block_to_node_olist(self):
        node = text_block_to_html_node("1. item 1\n2. item 2")
        self.assertEqual(
            "<div><ol><li>item 1</li><li>item 2</li></ol></div>", node.to_html()
        )

    def test_block_to_node_code(self):
        node = text_block_to_html_node(
            "```This is text that _should_ remain\nthe **same** even with inline stuff\n```"
        )
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            node.to_html(),
        )

    def test_block_to_node_heading(self):
        node = text_block_to_html_node("# heading 1")
        self.assertEqual("<div><h1>heading 1</h1></div>", node.to_html())

    def test_block_to_node_heading6(self):
        node = text_block_to_html_node("###### heading 6")
        self.assertEqual("<div><h6>heading 6</h6></div>", node.to_html())
