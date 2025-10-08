import unittest

from src.htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
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


if __name__ == "__main__":
    _ = unittest.main()
