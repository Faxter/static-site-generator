import unittest

from src.htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"key1": "value1"})
        expected = ' key1="value1"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_two_props(self):
        node = HTMLNode(props={"key1": "value1", "key2": "value2"})
        expected = ' key1="value1" key2="value2"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_props_empty(self):
        node = HTMLNode()
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_eq_empty_node(self):
        self.assertEqual(HTMLNode(), HTMLNode())

    def test_eq_simple_node(self):
        node1 = HTMLNode("tag", "value")
        node2 = HTMLNode("tag", "value")
        self.assertEqual(node1, node2)

    def test_neq_simple_node(self):
        node1 = HTMLNode("tag", "value")
        node2 = HTMLNode("tag", "blergh")
        self.assertNotEqual(node1, node2)

    def test_eq_with_children(self):
        node1 = HTMLNode("tag", "value", [HTMLNode("a")])
        node2 = HTMLNode("tag", "value", [HTMLNode("a")])
        self.assertEqual(node1, node2)

    def test_neq_with_children(self):
        node1 = HTMLNode("tag", "value", [HTMLNode("a")])
        node2 = HTMLNode("tag", "value", [HTMLNode("b")])
        self.assertNotEqual(node1, node2)

    def test_eq_with_props(self):
        node1 = HTMLNode("tag", "value", [HTMLNode("a")], {"p": "q"})
        node2 = HTMLNode("tag", "value", [HTMLNode("a")], {"p": "q"})
        self.assertEqual(node1, node2)

    def test_neq_with_props(self):
        node1 = HTMLNode("tag", "value", [HTMLNode("a")], {"p": "q"})
        node2 = HTMLNode("tag", "value", [HTMLNode("a")], {"p": "r"})
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    _ = unittest.main()
