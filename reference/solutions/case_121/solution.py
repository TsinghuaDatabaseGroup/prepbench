from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import re


def _normalize(s: str) -> str:
    if s is None:
        return ""
    s2 = re.sub(r"\s+", " ", str(s)).strip()
    return s2


def _norm_key(s: str) -> str:
    return _normalize(s).casefold()


def _smash(name: str, answer: str) -> str:
    n = _normalize(name)
    a = _normalize(answer)
    n_low = n.casefold()
    a_low = a.casefold()
    max_k = 0
    max_possible = min(len(n_low), len(a_low))
    for k in range(1, max_possible + 1):
        if n_low.endswith(a_low[:k]):
            max_k = k
    return n + a[max_k:]


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_smash = pd.read_csv(inputs_dir / 'input_01.csv')
    df_names = pd.read_csv(inputs_dir / 'input_02.csv')
    df_q = pd.read_csv(inputs_dir / 'input_03.csv')

    raw = pd.read_csv(inputs_dir / 'input_04.csv', header=None, names=['raw'])
    cat = raw['raw'].astype(str).str.split(':', n=1, expand=True)
    cat.columns = ['Category', 'Answer']
    cat['Category'] = cat['Category'].astype(str).str.strip()
    cat['Answer'] = cat['Answer'].astype(str).str.strip()
    df_answers = cat

    names_list: List[str] = [ _normalize(x) for x in df_names['Name'].tolist() ]
    answers_list: List[Tuple[str, str]] = [ (_normalize(r.Category), _normalize(r.Answer)) for r in df_answers.itertuples(index=False) ]

    results: List[Tuple[int, str, str, str, str]] = []

    for row in df_smash.itertuples(index=False):
        qno = int(row[0])
        smash_val = _normalize(row[1])
        smash_key = _norm_key(smash_val)

        matched_name = None
        matched_answer = None

        found = False
        for name in names_list:
            for _, ans in answers_list:
                cand = _smash(name, ans)
                if _norm_key(cand) == smash_key:
                    matched_name = name
                    matched_answer = ans
                    found = True
                    break
            if found:
                break

        if not found:
            for name in names_list:
                for _, ans in answers_list:
                    cand = _normalize(name) + _normalize(ans)
                    if _norm_key(cand) == smash_key:
                        matched_name = _normalize(name)
                        matched_answer = _normalize(ans)
                        found = True
                        break
                if found:
                    break

        question = df_q.loc[df_q['Q No'] == qno, 'Question'].iloc[0]

        results.append((qno, _normalize(question), matched_answer if matched_answer is not None else "", matched_name if matched_name is not None else "", smash_val))

    out = pd.DataFrame(results, columns=["Q No", "Question", "Answer", "Name", "Answer Smash"])

    out["Q No"] = pd.to_numeric(out["Q No"], errors='coerce')
    out = out.sort_values(["Q No"]).reset_index(drop=True)

    return {"output_01.csv": out[["Q No", "Question", "Answer", "Name", "Answer Smash"]]}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'
    cand_dir = task_dir / 'cand'
    cand_dir.mkdir(parents=True, exist_ok=True)
    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        df.to_csv(cand_dir / fname, index=False, encoding='utf-8')
    for fname in outputs.keys():
        print(str(cand_dir / fname))





