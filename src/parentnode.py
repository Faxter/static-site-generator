from typing import final, override
from src.htmlnode import HTMLNode


@final
class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    @override
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag of ParentNode must be set")
        if self.children is None:
            raise ValueError("ParentNode must have children")

        children = ""
        for child in self.children:
            children += child.to_html()
        return f"<{self.tag}{super().props_to_html()}>{children}</{self.tag}>"
