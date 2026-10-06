import csv

CLEAR = ("resolved", "waiting for docs", "please close", "issue fixed", "docs received")

def is_clear(note):
    text = note.lower()
    return any(word in text for word in CLEAR)

def main():
    closed = []
    unclear = []
    with open("grey_notes.csv", newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0] == "case_id":
                continue
            case_id = row[0]
            note = ",".join(row[1:])
            item = {"case_id": case_id, "note": note}
            if is_clear(note):
                closed.append(item)
            else:
                unclear.append(item)
    with open("closed.csv", "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=["case_id", "note"])
        writer.writeheader()
        writer.writerows(closed)
    print(f"closed {len(closed)}")
    for row in unclear:
        print(row["case_id"], row["note"])

if __name__ == "__main__":
    main()