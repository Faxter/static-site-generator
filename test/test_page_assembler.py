import unittest

from src.page_assembler import (
    extract_title_from_markdown,
    generate_page,
)


class TestPageAssembler(unittest.TestCase):
    def test_generate_single_page(self):
        html = generate_page(
            "# title 1\n\nsome very interesting text",
            "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>",
        )
        self.assertEqual(
            "<html><title>title 1</title><body><div><h1>title 1</h1><p>some very interesting text</p></div></body></html>",
            html,
        )

    def test_extract_title(self):
        title = extract_title_from_markdown("# title 1\n\nfirst paragraph!")
        self.assertEqual("title 1", title)

    def test_extract_title_no_title_in_doc(self):
        with self.assertRaises(Exception):
            extract_title_from_markdown("just plain text")
