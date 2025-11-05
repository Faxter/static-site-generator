import unittest

from src.textnode import TextType, TextNode
from src.leafnode import LeafNode
from src.node_conversion import (
    split_text_nodes_by_delimiter,
    text_node_to_html_node,
    extract_markdown_images,
    extract_markdown_links,
    split_text_nodes_by_image,
    split_text_nodes_by_link,
)


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
        self.assertListEqual(
            [
                TextNode("Some ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_text_by_delimiter_without_delimiter_in_text(self):
        node = TextNode("Some not so bold text", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("Some not so bold text", TextType.PLAIN)], new_nodes
        )

    def test_split_text_by_delimiter_with_delimiter_at_start(self):
        node = TextNode("**bold** text at start", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text at start", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_text_by_delimiter_with_delimiter_at_end(self):
        node = TextNode("text with **bold**", TextType.PLAIN)
        new_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("text with ", TextType.PLAIN), TextNode("bold", TextType.BOLD)],
            new_nodes,
        )

    def test_split_text_by_two_delimiters(self):
        node = TextNode("text with **bold** and _italic_ text", TextType.PLAIN)
        bolded_nodes = split_text_nodes_by_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_text_nodes_by_delimiter(bolded_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("text with ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_extract_markdown_images_one_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images("just some text")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_one_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
            ],
            matches,
        )

    def test_extract_markdown_links_two_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links("This is text without a link")
        self.assertListEqual(
            [],
            matches,
        )

    def test_split_text_for_images_one_image_at_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_text_nodes_by_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_text_for_images_one_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the start",
            TextType.PLAIN,
        )
        new_nodes = split_text_nodes_by_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the start", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_text_for_images_one_image_in_middle(self):
        node = TextNode(
            "An ![image](https://i.imgur.com/zjjcJKZ.png) in the middle",
            TextType.PLAIN,
        )
        new_nodes = split_text_nodes_by_image([node])
        self.assertListEqual(
            [
                TextNode("An ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in the middle", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_text_for_images_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_text_nodes_by_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
