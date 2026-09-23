# Milestone 1 — starter baseline

Recorded on 2026-09-23 before changing the chunker. Corpus: `campus_life`.
The first four documents read were the posts on add/drop, campus jobs,
declaring a major, and dining dollars. These are short titled posts with
closely related rules in the same paragraph. Splitting the rule from its
exception would remove useful context.

`python test.py`: 10 passed, 0 failed, 0 warnings, 0 skipped, including a
real Gemini response and the real 384-dimensional ONNX embedding model.

`python app.py index`:

```text
88 documents, 27,908 characters, ~317 characters per document
88 chunks, 317 characters on average (shortest 178, longest 549)
produced by chunker.py::fallback_split
```

`python app.py ask "is the housing lottery random?"`:

```text
best distance 0.254, cutoff 0.6

No, the housing lottery is not entirely random. While rising sophomores get a number drawn at random, juniors and seniors are ordered by accumulated credit hours first, with random selection used only as a tie-breaker (admin_housing_lottery.txt).

Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, housing_morrow_house.txt, housing_tamsin_court.txt
```

Special activity: `python app.py --corpus advice_threads chunks -n 1`
reported **26** chunks total using the original chunker.

No fake embeddings or fabricated model responses were used.
