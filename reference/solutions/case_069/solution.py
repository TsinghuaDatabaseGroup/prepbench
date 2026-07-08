import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    participants_df = pd.read_csv(inputs_dir / "input_01.csv")
    correct_answers_df = pd.read_csv(inputs_dir / "input_02.csv")
    
    correct_answers_dict = {}
    for _, row in correct_answers_df.iterrows():
        round_name = row['Round']
        answers_str = row['Answers']
        answers_list = [a.strip() for a in answers_str.split(',')]
        correct_answers_dict[round_name] = answers_list
    
    results = []
    
    for _, participant_row in participants_df.iterrows():
        name = participant_row['Name']
        round_scores = {}
        total_score = 0
        
        for round_num in range(1, 6):
            round_name = f'Round{round_num}'
            participant_answers_str = participant_row[round_name]
            
            participant_answers = [a.strip() for a in participant_answers_str.rstrip().split(',')]
            correct_answers = correct_answers_dict[round_name]
            
            correct_count = 0
            for i in range(len(participant_answers)):
                if i < len(correct_answers) and participant_answers[i] == correct_answers[i]:
                    correct_count += 1
            
            round_scores[round_name] = correct_count
            total_score += correct_count
        
        result = {
            'Name': name,
            **round_scores,
            'Total Score': total_score
        }
        results.append(result)
    
    output_df = pd.DataFrame(results)
    
    output_df = output_df.sort_values('Total Score', ascending=False).reset_index(drop=True)
    
    positions = []
    position = 1
    prev_score = None
    
    for score in output_df['Total Score']:
        if prev_score is None or score != prev_score:
            if prev_score is not None:
                position += 1
        positions.append(position)
        prev_score = score
    
    output_df['Position'] = positions
    
    output_df = output_df[['Round1', 'Round2', 'Round3', 'Round4', 'Round5', 'Total Score', 'Position', 'Name']]
    
    return {
        'output_01.csv': output_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for name, df in outputs.items():
        df.to_csv(cand_dir / name, index=False, encoding='utf-8')

