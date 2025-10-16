from src.textnode import TextType, TextNode
from src.leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(text_node.text, None)
        case _:
            raise ValueError("invalid text type in TextNode")
