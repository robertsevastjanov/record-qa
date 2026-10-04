import csv
from datetime import datetime

ALLOWED = {"open", "pending", "closed"}

def issues_for(row, seen_ids):
    problems = []
    case_id = row["case_id"]
    if case_id != case_id.strip() or not case_id.strip():
        problems.append("bad case_id")
    if case_id in seen_ids:
        problems.append("duplicate case_id")
    seen_ids.add(case_id)
    if not row["user_id"].strip():
        problems.append("empty user_id")
    if row["status"] not in ALLOWED:
        problems.append("bad status")
    try:
        datetime.strptime(row["opened_at"], "%Y-%m-%d")
    except ValueError:
        problems.append("bad date")
    try:
        amount = float(row["amount"])
        if amount < 0:
            problems.append("negative amount")
    except ValueError:
        problems.append("amount not a number")
    if row["status"] == "closed" and not row["note"].strip():
        problems.append("closed without note")
    return problems

def main():
    seen = set()
    bad = 0
    total = 0
    with open("cases.csv", newline="", encoding="utf-8") as f, open("report.csv", "w", newline="", encoding="utf-8") as out:
        reader = csv.DictReader(f)
        writer = csv.writer(out)
        writer.writerow(["row", "case_id", "issues"])
        for i, row in enumerate(reader, start=2):
            total += 1
            problems = issues_for(row, seen)
            if problems:
                bad += 1
                writer.writerow([i, row["case_id"], "; ".join(problems)])
    print(f"checked {total}, bad {bad}, clean {total - bad}")

if __name__ == "__main__":
    main()
