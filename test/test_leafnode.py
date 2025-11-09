import unittest

from src.leafnode import LeafNode, text_node_to_html_node
from src.textnode import TextNode, TextType


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_empty_tag(self):
        node = LeafNode(tag=None, value="Franz")
        self.assertEqual(node.to_html(), "Franz")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode(tag=None, value="")
        node.value = None
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_leaf_node_to_html_a_with_props(self):
        node = LeafNode(
            tag="a", value="LinkText", props={"href": "https://faxxter.com"}
        )
        self.assertEqual(node.to_html(), '<a href="https://faxxter.com">LinkText</a>')

    def test_plain_text_to_html(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text_to_html(self):
        html_node = text_node_to_html_node(TextNode("some bold text", TextType.BOLD))
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "some bold text")

    def test_italic_text_to_html(self):
        html_node = text_node_to_html_node(
            TextNode("some italic text", TextType.ITALIC)
        )
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "some italic text")

    def test_code_text_to_html(self):
        html_node = text_node_to_html_node(TextNode("some code text", TextType.CODE))
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "some code text")

    def test_link_text_to_html(self):
        html_node = text_node_to_html_node(
            TextNode("some link text", TextType.LINK, "https://faxxter.com")
        )
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "some link text")
        self.assertEqual(html_node.props, {"href": "https://faxxter.com"})

    def test_image_text_to_html(self):
        html_node = text_node_to_html_node(
            TextNode(
                "image description", TextType.IMAGE, "https://faxxter.com/image.png"
            )
        )
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"alt": "image description", "src": "https://faxxter.com/image.png"},
        )
