"""Check the strict cutoff and that refusals do not call the model."""

import unittest
from unittest.mock import patch

import gate
from app import ask_pipeline
from store import Result


class GateTests(unittest.TestCase):
    def test_empty_results_refuse(self):
        self.assertFalse(gate.check([], threshold=2).passed)

    def test_exact_cutoff_refuses_and_nearer_match_passes(self):
        hit = Result("text", "source.txt", "source.txt#0", 0.61, "test")
        self.assertFalse(gate.check([hit], threshold=0.61).passed)
        hit.distance = 0.609
        self.assertTrue(gate.check([hit], threshold=0.61).passed)

    def test_refusal_stops_before_generation(self):
        hit = Result("unrelated", "source.txt", "source.txt#0", 0.9, "test")
        with patch("store.search", return_value=[hit]), patch("generate.answer_from_chunks") as model:
            outcome = ask_pipeline("unrelated question", threshold=0.61)
        model.assert_not_called()
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["answer"], gate.REFUSAL)
        self.assertIsNone(outcome["prompt"])
        self.assertEqual(outcome["sources"], [])
