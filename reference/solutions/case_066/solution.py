import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    encrypted_df = pd.read_csv(inputs_dir / "input_01.csv")
    cipher_df = pd.read_csv(inputs_dir / "input_03.csv")
    
    encrypted_message = encrypted_df["Encrypted Message"].dropna().iloc[0]
    
    cipher_df = cipher_df.dropna(subset=['Alphabet', 'Cipher'])
    cipher_map = dict(zip(cipher_df['Cipher'], cipher_df['Alphabet']))
    
    characters = []
    positions = []
    for pos, char in enumerate(encrypted_message):
        characters.append(char)
        positions.append(pos)
    
    chars_df = pd.DataFrame({
        'position': positions,
        'encrypted_char': characters
    })
    
    def decode_char(char):
        if char == ' ':
            return ' '
        elif char in cipher_map:
            return cipher_map[char]
        else:
            return char
    
    chars_df['decoded_char'] = chars_df['encrypted_char'].apply(decode_char)
    
    chars_df = chars_df.sort_values('position').reset_index(drop=True)
    
    decoded_message = ''.join(chars_df['decoded_char'].tolist())
    
    output_df = pd.DataFrame({
        'Decoded Message': [decoded_message]
    })
    
    return {'output_01.csv': output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

