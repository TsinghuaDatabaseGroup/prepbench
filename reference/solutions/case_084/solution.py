import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    def is_anagram(word1: str, word2: str) -> bool:
        w1 = str(word1).lower().strip()
        w2 = str(word2).lower().strip()
        
        if len(w1) != len(w2):
            return False
        
        return sorted(w1) == sorted(w2)
    
    df["Anagram?"] = df.apply(
        lambda row: "Yes" if is_anagram(row["Word 1"], row["Word 2"]) else "No",
        axis=1
    )
    
    output = df[["Word 1", "Word 2", "Anagram?"]].copy()
    
    return {"output_01.csv": output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

