from typing import final, override
from enum import Enum


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


@final
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str):
        self.text = text
        self.text_type = text_type
        self.url = url if len(url) > 0 else None

    @override
    def __eq__(self, other: object):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    @override
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url}"
