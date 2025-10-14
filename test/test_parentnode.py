import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_no_tag(self):
        node = ParentNode(tag="", children=[])
        node.tag = None
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_parent_children_missing_value(self):
        node = ParentNode(tag="", children=[LeafNode("", "")])
        node.children[0].value = None
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_parent_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


"""
    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
"""
