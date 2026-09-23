# Criteria self-check (before retrieval tuning)

AI was asked to state exactly how to test the five criteria without proposing
changes. These are testing procedures, not results.

1. Retrieve the configured top five chunks for each of the five questions.
   Read them against the question and original source, and count questions
   with at least one chunk containing the answer. Require at least four.
2. Read each generated answer and check for at least one source filename.
   Gate refusals are excluded as specified under criterion 2.
3. Retrieve once for each fixed `OUT_OF_SCOPE` question, then run the gate.
   Count cases where it stops before generation and returns the stated
   refusal (allowing the documented terminal period). Require at least four.
4. Run the exact sample command. Compare each of its five chunks with its
   source; check for the title, a complete body sentence, and uncut sentence
   boundaries. All five must pass.
5. For each generated answer, test the expected phrase case-insensitively
   and read each factual claim against the files that answer cites. Count
   only answers passing both checks; require at least four. Literal phrase
   matching can fail on valid paraphrases, so record that honestly.
