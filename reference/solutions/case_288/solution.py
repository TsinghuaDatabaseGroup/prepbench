from pathlib import Path
from typing import Dict
import pandas as pd
from datetime import datetime, date, timedelta


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    students = pd.read_csv(inputs_dir / "input_01.csv")
    terms = pd.read_csv(inputs_dir / "input_02.csv")

    def parse_human_date(s: str) -> date:
        return datetime.strptime(s, "%A %d %B %Y").date()

    term_rows = []
    for _, r in terms.iterrows():
        term_name = str(r["Term"])
        start_d = parse_human_date(str(r["Starts"]))
        end_d = parse_human_date(str(r["Ends"]))
        term_rows.append((term_name, start_d, end_d))

    def is_teaching_term(name: str) -> bool:
        nl = name.lower()
        if "half term" in nl or "holiday" in nl or "bank holiday" in nl:
            return False
        return ", term" in nl

    teaching_terms = [(n, s, e)
                      for (n, s, e) in term_rows if is_teaching_term(n)]
    holidays = [(n, s, e)
                for (n, s, e) in term_rows if not is_teaching_term(n)]

    teaching_terms_sorted = sorted(teaching_terms, key=lambda x: x[1])
    first_term_start = teaching_terms_sorted[0][1]

    def in_any(range_list, d: date):
        for item in range_list:
            _, s, e = item
            if s <= d <= e:
                return True, item
        return False, None

    def is_school_day(d: date) -> bool:
        if d.weekday() >= 5:
            return False
        inside, _ = in_any(teaching_terms_sorted, d)
        if not inside:
            return False
        h, _ = in_any(holidays, d)
        if h:
            return False
        return True

    def last_friday_in_term(term_tuple):
        _, s, e = term_tuple
        d = e
        while d >= s:
            if d.weekday() == 4 and is_school_day(d):
                return d
            d -= timedelta(days=1)
        return e

    def last_friday_of_previous_term(before_date: date):
        prev = None
        for item in teaching_terms_sorted:
            _, s, e = item
            if e < before_date:
                prev = item
            else:
                break
        lf = last_friday_in_term(prev)
        _, s, e = prev
        if e.weekday() in (0, 1) and (e - lf).days <= 4:
            return e
        return lf

    dob = pd.to_datetime(students["Date of Birth"], dayfirst=False)
    students["dob_month"] = dob.dt.month
    students["dob_day"] = dob.dt.day

    def school_year_birthday(m: int, d: int):
        m = int(m)
        d = int(d)
        year = 2024 if m >= 9 else 2025
        return date(year, m, d)

    students["birthday"] = [school_year_birthday(m, d) for m, d in zip(
        students["dob_month"], students["dob_day"])]

    def compute_cake_day(bd):
        if bd < first_term_start:
            return None
        if is_school_day(bd):
            return bd
        if bd.weekday() >= 5:
            fri = bd - timedelta(days=(bd.weekday() - 4))
            return fri if is_school_day(fri) else last_friday_of_previous_term(bd)
        return last_friday_of_previous_term(bd)

    students["cake_day"] = [compute_cake_day(
        bd) for bd in students["birthday"]]

    cake = students.dropna(subset=["cake_day"]).copy()

    cake["Cake Needed On Date"] = pd.to_datetime(
        cake["cake_day"]).dt.strftime("%d/%m/%Y")
    cake["Cake Weekday"] = [pd.to_datetime(
        d).strftime("%A") for d in cake["cake_day"]]

    out = cake.groupby(["Cake Needed On Date", "Cake Weekday"], as_index=False).size(
    ).rename(columns={"size": "Count of Cakes"})
    out = out[["Cake Needed On Date", "Cake Weekday", "Count of Cakes"]]
    out["Count of Cakes"] = out["Count of Cakes"].astype(int)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
