"""Record one real unit-1 verification pass; not the unit-2 three-run evaluation.

Run after indexing: python tools/check_unit1.py
Uses real embeddings and five uncached model calls. Never changes targets.
"""

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
import gate
from app import ask_pipeline
from chunker import split_documents
from ingest import load_documents
from questions import QUESTIONS, OUT_OF_SCOPE
from store import search


def main():
    if len(QUESTIONS) != 5 or len(OUT_OF_SCOPE) != 5:
        raise ValueError("This check requires five in-scope and five out-of-scope questions")
    config.CACHE_ENABLED = False
    rows = []
    for entry in QUESTIONS:
        hits = search(entry["question"])
        outcome = ask_pipeline(entry["question"])
        row = {**entry, **outcome, "in_corpus": True,
               "results": [asdict(hit) for hit in hits],
               "expects_found": entry["expects"].casefold() in outcome["answer"].casefold(),
               "retrieved_filename_in_answer": any(hit.source in outcome["answer"] for hit in hits)}
        rows.append(row)
        print(entry["question"], flush=True)
        print(outcome["answer"], flush=True)

    for question in OUT_OF_SCOPE:
        # Any generation attempt here is a failure, not a fake answer.
        with patch("generate.answer_from_chunks", side_effect=AssertionError("Gate allowed an off-topic model call")) as model:
            outcome = ask_pipeline(question)
            model.assert_not_called()
        assert outcome["refused"] and outcome["answer"] == gate.REFUSAL
        rows.append({**outcome, "in_corpus": False, "model_calls": 0})
        print(f"REFUSED {outcome['best_distance']:.6f}: {question}", flush=True)

    chunks = split_documents(load_documents())
    sample = chunks[::max(len(chunks) // 5, 1)][:5]
    payload = {"recorded_at": datetime.now(timezone.utc).isoformat(),
               "corpus": config.CORPUS, "model": config.MODEL,
               "embedding_model": config.EMBEDDING_MODEL, "top_k": config.TOP_K,
               "threshold": config.THRESHOLD, "cache": False,
               "samples": [asdict(chunk) for chunk in sample], "rows": rows}
    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / "unit1-verification.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Evidence saved to {path}")


if __name__ == "__main__":
    main()
