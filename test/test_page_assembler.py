import unittest
from pathlib import Path

from src.page_assembler import extract_title_from_markdown, generate_page


class TestPageAssembler(unittest.TestCase):
    def test_generate_page(self):
        html = generate_page(
            Path("test/content_example.md"),
            Path("test/template_example.html"),
        )
        with open("test/template_example.html", "r") as f:
            template_content = f.read()
        result = template_content.replace("{{ Title }}", "title 1").replace(
            "{{ Content }}",
            "<div><h1>title 1</h1><p>some very interesting text</p></div>",
        )
        self.assertEqual(result, html)

    def test_extract_title(self):
        title = extract_title_from_markdown("# title 1\n\nfirst paragraph!")
        self.assertEqual("title 1", title)

    def test_extract_title_no_title_in_doc(self):
        with self.assertRaises(Exception):
            extract_title_from_markdown("just plain text")
