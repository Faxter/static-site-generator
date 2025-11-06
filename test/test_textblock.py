import unittest

from src.textblock import BlockType, block_to_block_type


class TestTextBlock(unittest.TestCase):
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
