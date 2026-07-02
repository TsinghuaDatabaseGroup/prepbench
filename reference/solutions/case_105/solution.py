from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)

    df.columns = [c.strip() for c in df.columns]
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    df['MONEY'] = pd.to_numeric(df['MONEY'], errors='coerce')
    df['EVENTS'] = pd.to_numeric(df['EVENTS'], errors='coerce')

    df['money_per_event'] = df['MONEY'] / df['EVENTS']

    df['tour_rank'] = df.groupby('TOUR')['MONEY'].rank(
        method='dense', ascending=False)
    df['overall_rank'] = df['MONEY'].rank(method='dense', ascending=False)
    df['rank_diff'] = df['overall_rank'] - df['tour_rank']

    total_prize = df.groupby('TOUR', as_index=False)[
        'MONEY'].sum().set_index('TOUR')['MONEY']
    num_players = df.groupby('TOUR', as_index=False)[
        'PLAYER NAME'].size().set_index('TOUR')['size']
    total_events = df.groupby('TOUR', as_index=False)[
        'EVENTS'].sum().set_index('TOUR')['EVENTS']
    avg_money_per_event = (
        df.groupby('TOUR', as_index=False)[
            'money_per_event'].mean().set_index('TOUR')['money_per_event']
    )
    avg_rank_diff = df.groupby('TOUR', as_index=False)[
        'rank_diff'].mean().set_index('TOUR')['rank_diff']

    def make_row(measure: str, pga_val, lpga_val):
        return {
            'Measure': measure,
            'PGA': pga_val,
            'LPGA': lpga_val,
            'Difference between tours': lpga_val - pga_val,
        }

    pga_rank = round(float(avg_rank_diff.get('PGA', 0.0)), 2)
    lpga_rank = round(float(avg_rank_diff.get('LPGA', 0.0)), 2)
    diff_rank = round(lpga_rank - pga_rank, 2)
    row_avg_rank_diff = {
        'Measure': 'Avg Difference in Ranking',
        'PGA': pga_rank,
        'LPGA': lpga_rank,
        'Difference between tours': float(f"{diff_rank:.2f}")
    }

    row_avg_money_per_event = make_row(
        'Avg Money per Event',
        int(round(float(avg_money_per_event.get('PGA', 0.0)), 0)),
        int(round(float(avg_money_per_event.get('LPGA', 0.0)), 0)),
    )

    row_num_players = make_row(
        'Number of Players',
        int(num_players.get('PGA', 0)),
        int(num_players.get('LPGA', 0)),
    )

    row_num_events = make_row(
        'Number of Events',
        int(total_events.get('PGA', 0)),
        int(total_events.get('LPGA', 0)),
    )

    row_total_money = make_row(
        'Total Prize Money',
        int(total_prize.get('PGA', 0)),
        int(total_prize.get('LPGA', 0)),
    )

    out_df = pd.DataFrame([
        row_avg_rank_diff,
        row_avg_money_per_event,
        row_num_players,
        row_num_events,
        row_total_money,
    ], columns=['Measure', 'PGA', 'LPGA', 'Difference between tours'])

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).write_text('', encoding='utf-8')
        df.to_csv(cand_dir / fname, index=False, encoding='utf-8')
