import unittest

from src.leafnode import LeafNode
from src.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_parent_no_tag(self):
        node = ParentNode(tag="", children=[])
        node.tag = None
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_parent_no_children(self):
        node = ParentNode(tag="", children=[])
        node.children = None
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_parent_to_html_with_child(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="Italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
        )

    def test_parent_to_html_without_children(self):
        parent_node = ParentNode("p", [])
        self.assertEqual(parent_node.to_html(), "<p></p>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_to_html_with_props_in_child(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode(
                    tag="a", value="LinkText", props={"href": "https://faxxter.com"}
                )
            ],
        )
        self.assertEqual(
            parent_node.to_html(), '<p><a href="https://faxxter.com">LinkText</a></p>'
        )

    def test_parent_node_to_html_with_props_in_parent(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode(
                    tag="a", value="LinkText", props={"href": "https://faxxter.com"}
                )
            ],
            {"prop": "interesting"},
        )
        self.assertEqual(
            parent_node.to_html(),
            '<p prop="interesting"><a href="https://faxxter.com">LinkText</a></p>',
        )
