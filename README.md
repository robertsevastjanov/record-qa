# record-qa

Rule-based checker for high-volume case records.
Replaces the manual pass for a computer operator: duplicate ids, bad status, broken dates, empty required fields.

Run: python check.py
Found 8 bad rows out of 26.
SQL: duplicate ids via GROUP BY, 1 duplicate (C-1001).

python3 triage.py
Closes 5 clear notes into closed.csv and prints 5 unclear ones.
A comma inside the note is kept.

1st check. Unclear notes can be labeled by a local Llama 3.2 model: paid_unclear, fraud_unclear, or other.
The model does not close the case. One label was disagreed: C-2010.

2nd check. Llama labeled 5 unclear notes. 2 agreed, 3 disagreed. Cases stay open.

## Updated LLM triage workflow

`triage.py` now sends every input record to local Llama 3.2 via Ollama.
It validates the returned label and keeps every record for human review.
It no longer automatically closes cases. Existing closed.csv files are
historical outputs and are not updated by this workflow.

Reliability:
- 60-second inference timeout
- Subprocess failure handling
- Allowed-label validation
- manual_review label for invalid responses or execution failures
- JSONL logs containing case ID, model, duration, status, and error

Run:
    python3 triage.py

Run unit tests without starting Ollama:
    python3 -m unittest -v test_triage

Verification:
- Five unit tests passed, covering valid labels, invalid outputs,
  timeouts, process failures, and a missing executable.
- A local run processed 10 sample records.
- Output checks confirmed all 10 records require review and have logs.

These checks verify workflow behaviour, not classification accuracy.
