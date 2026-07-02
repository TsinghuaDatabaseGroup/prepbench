import pandas as pd
import re
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    scrabble_scores = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
        'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
        'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
        'Y': 4, 'Z': 10
    }
    
    def calculate_word_score(word: str) -> int:
        return sum(scrabble_scores.get(c.upper(), 0) for c in word)
    
    def is_poem_line(text: str) -> bool:
        if not text or pd.isna(text):
            return False
        
        text_upper = text.upper()
        cleaned = text.strip().replace('_x000D_', '').strip()
        
        if '<' in text or '>' in text:
            return False
        
        html_patterns = [
            r'<SCRIPT', r'</SCRIPT', r'<STYLE', r'</STYLE', r'<HEAD', r'</HEAD',
            r'<BODY', r'</BODY', r'<HTML', r'</HTML', r'<BR', r'<DIV', r'<P>',
            r'STYLE=', r'JAVASCRIPT', r'OBJECT\(\)', r'E9=', r'URCHIN', r'ADSBYGOOGLE',
            r'GOOGLE_AD', r'DATA-AD', r'WINDOW\.', r'PUSH\({}\)', r'_UACCT',
            r'SIZE =', r'728X90', r'468X60', r'336X280', r'300X250', r'300X600'
        ]
        for pattern in html_patterns:
            if re.search(pattern, text_upper):
                return False
        
        if '=' in cleaned and not any(c.isalpha() for c in cleaned[:20]):
            return False
        
        if len(cleaned) < 3:
            return False
        
        if not any(c.isalpha() for c in cleaned):
            return False
        
        if cleaned.count('=') > 1 or (cleaned.count(';') > 0 and '=' in cleaned):
            return False
        
        comment_patterns = [
            r'^Written in .+\.$',
            r'^Composed in .+\.$',
            r'^The next .+ poems .+\.$'
        ]
        for pattern in comment_patterns:
            if re.match(pattern, cleaned, re.IGNORECASE):
                return False
        
        return True
    
    df['is_poem'] = df['DownloadData'].apply(is_poem_line)
    df_poems = df[df['is_poem']].copy()
    
    df_poems['Line'] = df_poems['DownloadData'].str.replace('_x000D_', '', regex=False)
    df_poems['Line'] = df_poems['Line'].str.strip()
    
    df_poems['Line'] = df_poems['Line'].str.replace(r'^--+\s*', '', regex=True)
    df_poems['Line'] = df_poems['Line'].str.replace('--', '', regex=False)
    df_poems['Line'] = df_poems['Line'].str.strip()
    
    df_poems = df_poems.drop_duplicates(subset=['Poem', 'Line'])
    
    result_rows = []
    
    for poem_name in df_poems['Poem'].unique():
        poem_df = df_poems[df_poems['Poem'] == poem_name].copy()
        poem_df = poem_df.sort_values('RowID').reset_index(drop=True)
        
        if len(poem_df) > 0:
            line_num = 1
            for idx, row in poem_df.iterrows():
                line_text = row['Line']
                
                if not line_text or len(line_text.strip()) < 2:
                    continue
                
                words_text = line_text.replace("'", "").replace("-", "")
                words = re.findall(r'\b[A-Za-z]+\b', words_text)
                
                if not words:
                    continue
                
                word_num = 1
                for word in words:
                    score = calculate_word_score(word)
                    
                    result_rows.append({
                        'Poem': poem_name,
                        'Line #': line_num,
                        'Line': line_text,
                        'Word #': word_num,
                        'Word': word.upper(),
                        'Score': score
                    })
                    word_num += 1
                
                line_num += 1
    
    output_df = pd.DataFrame(result_rows)
    
    if len(output_df) > 0:
        poem_max_scores = output_df.groupby('Poem')['Score'].max()
        
        def is_highest_scoring(row):
            poem = row['Poem']
            max_score = poem_max_scores[poem]
            return row['Score'] == max_score
        
        output_df['Highest Scoring Word?'] = output_df.apply(is_highest_scoring, axis=1)
    else:
        output_df['Highest Scoring Word?'] = False
    
    output_df = output_df[['Poem', 'Line #', 'Line', 'Word #', 'Word', 'Score', 'Highest Scoring Word?']]
    
    output_df['Line #'] = output_df['Line #'].astype(int)
    output_df['Word #'] = output_df['Word #'].astype(int)
    output_df['Score'] = output_df['Score'].astype(int)
    output_df['Highest Scoring Word?'] = output_df['Highest Scoring Word?'].astype(bool)
    
    return {
        'output_01.csv': output_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
