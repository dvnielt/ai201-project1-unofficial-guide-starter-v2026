# Unit 1 source review

This is one development verification pass, not unit 2's three-run evaluation.
The exact questions, outputs, retrieved texts, and distances are recorded in
`unit1-verification.json` and `unit1-retrieval.json`.

## Retrieved material and answer support

1. Add deadline: the first result, `admin_add_drop_deadline.txt`, says adding
   closes at the end of the second week. The answer repeats that fact and
   cites this file. Other retrieved posts discuss course work or registration
   but are not necessary to answer the question.
2. Dining dollars: `admin_dining_dollars.txt` explicitly says the amount left
   in May disappears. The answer cites it and makes only that claim. Lower
   results about meal plans and dining hours do not supply the answer.
3. Kestrel Commons: the main post and follow-up both give 20 to 25 minutes
   between 12:15 and 1:00. The answer cites both. Halden and Ridgeway wait
   times in lower results describe different venues and were not used.
4. Aldridge laundry: both the dorm overview and laundry post say $1.75 for a
   wash and card only. The answer cites these files and preserves both facts.
5. Work-study: `admin_campus_jobs_and_financial_aid.txt` says these earnings
   don't count against aid the way ordinary income does. The answer cites it
   accurately, but uses “do not count” rather than the committed expected
   phrase “don't count”. It fails the literal phrase component of criterion 5.

Retrieval therefore contains the answer in 5/5 cases. Source attribution is
present and supports the answer in 5/5. Criterion 5 passes in 4/5, meeting
its original target without changing its expected phrases after the run.

## Chunks and refusals

All five README samples are exact outputs of `chunker.py::split_documents`.
Each includes a title and complete body sentences. The administrative post
keeps the deadline and transcript exception together; the two course posts
preserve course names and workload/assessment details; the dining follow-up
retains its venue; the dorm post retains the building and payment method.
All five meet criterion 4. The boundary tests also confirm that all 88 current
posts remain intact and that synthetic longer posts split at paragraphs.

All five out-of-scope questions were refused at cutoff 0.61. During those
pipeline calls, generation was replaced by a guard that raises if invoked;
it was never invoked. These are real retrieval results, not fake embeddings.
The exact refusal is “I don't have enough information about that.”

## Limits

The cutoff was fitted to these ten questions; the same examples are not an
independent test set. Near-topic unsupported questions may pass the gate.
The unchanged 88-chunk count is intentional for this short-post corpus;
there is no claim that the new chunker improved measured retrieval here.
Oversized paragraphs can exceed the soft character budget and may exceed
the embedding model's token window on other corpora. This configuration is
for campus_life, not a universal chunking strategy.
