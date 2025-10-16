import unittest

from src.textnode import TextType, TextNode
from src.leafnode import LeafNode
from src.node_conversion import text_node_to_html_node


class TestNodeConversion(unittest.TestCase):
    def test_plain_text_to_html(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_illegal_to_html(self):
        with self.assertRaises(ValueError):
            _ = text_node_to_html_node(TextNode("bad", None))
