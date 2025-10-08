import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_wo_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_w_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "linktext")
        node2 = TextNode("This is a text node", TextType.BOLD, "linktext")
        self.assertEqual(node1, node2)

    def test_ne_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Here be a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_ne_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_ne_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "linktext")
        node2 = TextNode("This is a text node", TextType.BOLD, "othertext")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    _ = unittest.main()
