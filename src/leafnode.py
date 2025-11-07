from typing import final, override

from src.htmlnode import HTMLNode
from src.textnode import TextNode, TextType


@final
class LeafNode(HTMLNode):
    def __init__(
        self, value: str, tag: str | None, props: dict[str, str] | None = None
    ):
        _ = super().__init__(tag=tag, value=value, props=props)
        self.children = None

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("leaf node needs to have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(text_node.text, None)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("", "img", {"alt": text_node.text, "img": text_node.url})
