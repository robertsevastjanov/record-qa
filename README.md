# record-qa

Rule-based checker for high-volume case records.
Replaces the manual pass for a computer operator: duplicate ids, bad status, broken dates, empty required fields.

Run: python check.py
Found 8 bad rows out of 26.
SQL: duplicate ids via GROUP BY, 1 duplicate (C-1001).

python3 triage.py
Closes 5 clear notes into closed.csv and prints 5 unclear ones.
A comma inside the note is kept.

Unclear notes can be labeled by a local Llama 3.2 model: paid_unclear, fraud_unclear, or other.
The model does not close the case. One label was disagreed: C-2010.
