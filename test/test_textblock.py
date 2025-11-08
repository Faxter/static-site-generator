import unittest

from src.textblock import (
    BlockType,
    block_to_block_type,
    block_to_line,
    markdown_to_text_blocks,
)


class TestTextBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_text_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_blocks(self):
        md = """
block 1



block 2
"""
        blocks = markdown_to_text_blocks(md)
        self.assertEqual(["block 1", "block 2"], blocks)

    def test_markdown_to_blocks_empty_block_at_end(self):
        md = """
block 1

block 2

"""
        blocks = markdown_to_text_blocks(md)
        self.assertEqual(["block 1", "block 2"], blocks)

    def test_text_block_paragraph(self):
        block = "some text"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_text_block_heading(self):
        block = "# heading"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, type)

    def test_text_block_smaller_heading(self):
        block = "##### heading"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, type)

    def test_text_block_code(self):
        block = "```code```"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, type)

    def test_text_block_code_multiline(self):
        block = "```code\nmore code```"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.CODE, type)

    def test_text_block_quote(self):
        block = "> quote"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, type)

    def test_text_block_quote_multiline(self):
        block = "> quote\n> more quote"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, type)

    def test_text_block_quote_multiline_with_empty_line(self):
        block = "> quote\n>\n> more quote"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.QUOTE, type)

    def test_text_block_unordered_list(self):
        block = "- list item"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, type)

    def test_text_block_unordered_list_multiline(self):
        block = "- list item\n- second item"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.UNORDERED_LIST, type)

    def test_text_block_ordered_list(self):
        block = "1. first"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, type)

    def test_text_block_ordered_list_multiline(self):
        block = "1. first\n2. second\n3. third"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.ORDERED_LIST, type)

    def test_text_block_ordered_list_wrong_start(self):
        block = "2. first\n3. second\n1. third"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_text_block_ordered_list_wrong_order(self):
        block = "1. first\n3. second\n2. third"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.PARAGRAPH, type)

    def test_block_to_line_paragraph_without_markdown(self):
        line = block_to_line("text without markdown", BlockType.PARAGRAPH)
        self.assertEqual("text without markdown", line)

    def test_block_to_line_paragraph(self):
        line = block_to_line("**bold** text in _here_", BlockType.PARAGRAPH)
        self.assertEqual("**bold** text in _here_", line)

    def test_block_to_line_quote(self):
        line = block_to_line("> some quote", BlockType.QUOTE)
        self.assertEqual("some quote", line)

    def test_block_to_line_quote_multiline(self):
        line = block_to_line("> some quote\n> more", BlockType.QUOTE)
        self.assertEqual("some quote more", line)

    def test_block_to_line_ulist(self):
        lines = block_to_line("- one\n- two", BlockType.UNORDERED_LIST)
        self.assertListEqual(["one", "two"], lines)

    def test_block_to_line_olist(self):
        lines = block_to_line("1. one\n2. two", BlockType.ORDERED_LIST)
        self.assertListEqual(["one", "two"], lines)

    def test_block_to_line_code(self):
        line = block_to_line("```code stuff\nin here```", BlockType.CODE)
        self.assertEqual("code stuff\nin here", line)

    def test_block_to_line_heading(self):
        line = block_to_line("# heading 1", BlockType.HEADING)
        self.assertEqual("heading 1", line[1])
