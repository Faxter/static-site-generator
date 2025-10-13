import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_empty_tag(self):
        node = LeafNode(tag=None, value="Franz")
        self.assertEqual(node.to_html(), "Franz")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode(tag=None, value="")
        _ = node.to_html()
        _ = self.assertRaises(ValueError)

    def test_leaf_node_to_html_a_with_props(self):
        node = LeafNode(
            tag="a", value="LinkText", props={"href": "https://faxxter.com"}
        )
        self.assertEqual(node.to_html(), '<a href="https://faxxter.com">LinkText</a>')


if __name__ == "__main__":
    _ = unittest.main()
