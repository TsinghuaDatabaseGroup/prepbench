import pandas as pd
from pathlib import Path
import re
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"

    try:
        lines = input_file.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        lines = input_file.read_text(encoding="utf-8").splitlines()

    lines = lines[1:]

    pat1 = re.compile(r'^"(?P<battle>.*?)"",\'(?P<html>.*)$')
    pat2 = re.compile(r'^"(?P<battle>.*?)"\s*,\'(?P<html>.*)$')

    records = []
    for raw in lines:
        m = pat1.match(raw) or pat2.match(raw)
        if not m:
            continue
        battle = m.group("battle").strip()
        html = m.group("html").strip()
        if html.endswith('"'):
            html = html[:-1]

        parts = [p.strip() for p in html.split('<br />')]
        parts_plain = [re.sub(r'<[^>]+>', '', p).strip() for p in parts]

        battle_from_html = None
        for p in parts:
            if 'font-weight:bold' in p:
                mm = re.search(r'>([^<]+)<', p)
                if mm:
                    battle_from_html = mm.group(1).strip()
                    break
        if not battle_from_html:
            for plain in parts_plain:
                if plain and 'Battle' in plain:
                    battle_from_html = plain
                    break
        if battle_from_html:
            battle = battle_from_html

        date_str = None
        seen_title = False
        for p, plain in zip(parts, parts_plain):
            if not seen_title and (('font-weight:bold' in p) or (battle and battle in plain)):
                seen_title = True
                continue
            if seen_title and plain and ('Victors' not in plain):
                date_str = plain
                break

        war_str = None
        after_date = False
        for plain in parts_plain:
            if date_str and plain == date_str:
                after_date = True
                continue
            if after_date:
                if 'Victors' in plain:
                    break
                if plain:
                    war_str = plain
                    break

        victors_str = None
        victors_pos = None
        for i, p in enumerate(parts):
            if 'Victors:' in p:
                mm = re.search(r'Victors:\s*([^<]+)', p)
                if mm:
                    victors_str = mm.group(1).strip()
                else:
                    plain = re.sub(r'<[^>]+>', '', p)
                    idx = plain.find('Victors:')
                    if idx != -1:
                        victors_str = plain[idx+8:].strip()
                victors_pos = i
                break
        if victors_str is None and war_str:
            try:
                war_idx = parts_plain.index(war_str)
                for j in range(war_idx+1, len(parts_plain)):
                    q = parts_plain[j]
                    if q:
                        victors_str = q
                        victors_pos = j
                        break
            except ValueError:
                pass

        desc_str = None
        if victors_pos is not None:
            tail = [t for t in parts_plain[victors_pos+1:] if t]
            if tail:
                desc_str = ' '.join(tail)

        if all([battle, date_str, war_str, victors_str, desc_str]):
            records.append({
                'Battle': battle,
                'Date': date_str,
                'War': war_str,
                'Victors': victors_str,
                'Description': desc_str
            })

    if not records:
        return {"output_01.csv": pd.DataFrame(columns=['Date', 'Battle', 'War', 'Victors', 'Description'])}

    df = pd.DataFrame(records)

    def norm_date(s: str):
        if pd.isna(s):
            return None
        s = str(s).strip()
        if ',' in s and ('-' in s or ' - ' in s):
            t = s.replace(' - ', '-').strip()
            m = re.match(r'^(\d{1,2})-\d{1,2}\s+([A-Za-z]+),\s*(\d{4})$', t)
            if m:
                d1, mon, yr = m.groups()
                s = f"{int(d1)} {mon}, {yr}"
            else:
                left, year = t.split(',', 1)
                left = left.strip()
                year = year.strip()
                day = re.split(r'-', left.split()[0])[0]
                month = left.split()[-1]
                s = f"{int(day)} {month}, {year}"
        if re.fullmatch(r'\d{4}', s):
            return f"01/01/{int(s):04d}"
        if s.endswith('AD'):
            try:
                y = int(s.replace('AD', '').strip())
                return f"01/01/{y:04d}"
            except Exception:
                pass
        for fmt in ('%d %B, %Y', '%B %d, %Y', '%d %B %Y', '%B %d %Y'):
            try:
                dt = datetime.strptime(s, fmt)
                return dt.strftime('%d/%m/%Y')
            except Exception:
                continue
        return None

    df['Date'] = df['Date'].apply(norm_date)
    df = df[df['Date'].notna()].copy()

    def clean_text(x):
        if pd.isna(x):
            return x
        t = str(x)
        t = t.replace('Ł', '£')
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    for col in ['Battle', 'War', 'Victors']:
        df[col] = df[col].apply(clean_text)
    df['Description'] = df['Description'].astype(
        str).apply(lambda x: x.replace('Ł', '£').strip())

    out = df[['Date', 'Battle', 'War', 'Victors', 'Description']]
    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8-sig", lineterminator='\r\n')
