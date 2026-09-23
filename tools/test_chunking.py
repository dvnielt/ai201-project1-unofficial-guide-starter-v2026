"""Boundary and preservation checks: python -m unittest discover -s tools -p 'test_*.py'."""

import unittest
from unittest.mock import patch

import config
from chunker import split_documents
from ingest import Document, clean_text, load_documents


class ChunkingTests(unittest.TestCase):
    def test_current_posts_preserve_every_character_and_source(self):
        documents = load_documents("campus_life")
        chunks = split_documents(documents)
        self.assertEqual(len(chunks), len(documents))
        self.assertEqual([(c.source, c.text) for c in chunks],
                         [(d.source, d.text) for d in documents])
        self.assertTrue(all(c.produced_by == "chunker.py::split_documents" for c in chunks))

    def test_long_post_repeats_title_without_dropping_or_repeating_body(self):
        paragraphs = ["First paragraph has a complete thought.",
                      "Second paragraph describes a different detail.",
                      "Final paragraph records an exception."]
        with patch.object(config, "CHUNK_SIZE", 70):
            chunks = split_documents([Document("post.txt", "Title\n\n" + "\n\n".join(paragraphs))])
        self.assertEqual([c.index for c in chunks], [0, 1, 2])
        self.assertEqual([c.text for c in chunks], ["Title\n\n" + p for p in paragraphs])

    def test_oversized_paragraph_is_not_clipped_or_followed_by_a_tail(self):
        paragraph = "This sentence stays intact. " * 40
        chunks = split_documents([Document("long.txt", "Title\n\n" + paragraph)])
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].text, "Title\n\n" + paragraph.strip())

    def test_empty_and_single_paragraph_documents(self):
        chunks = split_documents([Document("empty.txt", " \n\n"), Document("single.txt", "One full sentence.")])
        self.assertEqual([(c.source, c.text) for c in chunks], [("single.txt", "One full sentence.")])

    def test_cleaning_preserves_paragraph_boundaries(self):
        self.assertEqual(clean_text("  Title\r\n\r\n\r\nBody\t\ttext.  "), "Title\n\nBody text.")


if __name__ == "__main__":
    unittest.main()
