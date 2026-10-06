import csv
import subprocess

CLEAR = ("resolved", "waiting for docs", "please close", "issue fixed", "docs received")

def is_clear(note):
    text = note.lower()
    return any(word in text for word in CLEAR)

def label(note):
    prompt = (
        "Label the note as paid_unclear, fraud_unclear, or other. "
        "Do not close the case. Reply with one label only.\nNote: " + note
    )
    result = subprocess.run(
        ["ollama", "run", "llama3.2"],
        input=prompt,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip().splitlines()[-1]

def main():
    closed = []
    unclear = []
    with open("grey_notes.csv", newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0] == "case_id":
                continue
            item = {"case_id": row[0], "note": ",".join(row[1:])}
            if is_clear(item["note"]):
                closed.append(item)
            else:
                unclear.append(item)
    with open("closed.csv", "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=["case_id", "note"])
        writer.writeheader()
        writer.writerows(closed)
    with open("queue.csv", "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["case_id", "note", "label"])
        for row in unclear:
            writer.writerow([row["case_id"], row["note"], label(row["note"])])
    print(f"closed {len(closed)}, queued {len(unclear)}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
