from typing import final, override
from src.htmlnode import HTMLNode


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
