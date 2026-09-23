# Acceptance criteria — campus life

Recorded before running the five test questions or tuning retrieval. The
starter's separate housing-lottery sanity check is recorded in
`results/milestone1.md`. AI drafted these criteria at the owner's explicit
request for this ungraded exercise; they are not represented as independently
student-authored criteria.

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** The questions mix policy deadlines, money, and dining
details. Similar dorm and dining posts can compete for the five retrieval
slots; allowing one miss makes room for that ambiguity without accepting
retrieval that fails on most topics.

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** All five in-corpus questions have named source files,
and those filenames are supplied to the model. Four cited answers would
leave one answer that cannot be checked. A gate refusal is a refusal to
answer, not a factual answer; it must not invent a source.

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that"
— in at least 4 of 5 tries.

**Why this target:** The five fixed `OUT_OF_SCOPE` questions cover unrelated
domains, but shared words may still produce a misleading embedding match.
One allowed miss acknowledges that limitation; two misses would let too
many unsupported questions reach generation. The application's period at
the end of the refusal does not change its meaning.

## 4. Sampled chunks retain complete thoughts

All five chunks printed by `python app.py chunks -n 5` must include a source
title and at least one complete body sentence, with no sentence cut in half
at either end.

**Why this target:** These short posts keep rules and exceptions together.
Even one clipped sample could omit an exception and mislead a reader, so
all five must stand on their own. This checks boundaries and context rather
than rewarding a particular character count.

## 5. Answers preserve the requested facts

For at least 4 of the 5 questions in `questions.py`, the generated answer
must contain its case-insensitive `expects` phrase and every factual claim
must be supported by the source documents cited in that answer.

**Why this target:** A deadline or price is not useful if it is replaced by
a vague summary. Four of five requires consistent precision while allowing
one wording failure; checking the cited documents also catches a fluent
answer that includes the expected phrase alongside invented details.
