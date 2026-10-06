# record-qa

Rule-based checker for high-volume case records. 
Replaces the manual pass for a computer operator: duplicate ids, bad status, broken dates, empty required fields. 

Run: python check.py

Found 8 bad rows out of 26

Unclear notes are labeled by a local Llama 3.2 model (paid_unclear, fraud_unclear, or other). It does not close the case. One label was disagreed: C-2010.

python3 triage.py closes 5 clear notes, prints 5 unclear.
