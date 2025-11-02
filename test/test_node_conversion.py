import unittest

from src.textnode import TextType, TextNode
from src.leafnode import LeafNode
from src.node_conversion import split_text_nodes_by_delimiter, text_node_to_html_node


class TestNodeConversion(unittest.TestCase):
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
            {"alt": "image description", "img": "https://faxxter.com/image.png"},
        )

    def test_split_text_without_delimiter(self):
        node = TextNode("Just some text", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "", TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "Just some text")

    def test_do_not_split_non_plain_text(self):
        node = TextNode("Just some bold text", TextType.BOLD)
        new_nodes = split_text_nodes_by_delimiter([node], ".", TextType.PLAIN)
        self.assertEqual(new_nodes[0].text, "Just some bold text")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_split_of_unmatched_delimiter_raises(self):
        node = TextNode("Just some **bold text", TextType.PLAIN)
        with self.assertRaises(Exception):
            _ = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)

    def test_split_text_by_delimiter(self):
        node = TextNode("Some **bold** text", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Some ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN)

    def test_split_text_by_delimiter_without_delimiter_in_text(self):
        node = TextNode("Some not so bold text", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Some not so bold text")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)

    def test_split_text_by_delimiter_with_delimiter_at_start(self):
        node = TextNode("**bold** text at start", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, " text at start")
        self.assertEqual(new_nodes[1].text_type, TextType.PLAIN)

    def test_split_text_by_delimiter_with_delimiter_at_end(self):
        node = TextNode("text with **bold**", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
