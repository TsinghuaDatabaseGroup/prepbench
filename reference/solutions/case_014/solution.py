
import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")

    df['Price'] = df['Price'].fillna(1.5)
    df['MemberID'] = df['MemberID'].fillna(0).astype(int)

    grouped = (
        df.groupby(['TicketID', 'MemberID', 'Type'])['Price']
        .agg(item_count='count', price_sum='sum')
        .reset_index()
    )

    rows = []
    for (ticket_id, member_id), ticket_rows in grouped.groupby(['TicketID', 'MemberID'], sort=True):
        counts = {row['Type']: row['item_count'] for _, row in ticket_rows.iterrows()}
        sums = {row['Type']: row['price_sum'] for _, row in ticket_rows.iterrows()}

        meal_deals = int(min(counts.get('Drink', 0), counts.get('Main', 0), counts.get('Snack', 0)))
        if meal_deals <= 0:
            continue

        total_ticket_price = sum(sums.get(item_type, 0.0) for item_type in ['Drink', 'Main', 'Snack'])
        total_excess = 0.0
        for item_type in ['Drink', 'Main', 'Snack']:
            item_count = counts.get(item_type, 0)
            average_price = (sums.get(item_type, 0.0) / item_count) if item_count else 0.0
            total_excess += (item_count - meal_deals) * average_price
        total_excess = float(Decimal(str(total_excess)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        meal_deal_earnings = meal_deals * 5
        rows.append({
            'Total Ticket Price': total_ticket_price,
            'Ticket Price Variance to Meal Deal Earnings': total_ticket_price - (meal_deal_earnings + total_excess),
            'Total Meal Deal Earnings': meal_deal_earnings,
            'Total Excess': total_excess,
            'TicketID': ticket_id,
            'MemberID': int(member_id),
        })

    output_df = pd.DataFrame(rows, columns=[
        'Total Ticket Price',
        'Ticket Price Variance to Meal Deal Earnings',
        'Total Meal Deal Earnings',
        'Total Excess',
        'TicketID',
        'MemberID'
    ])

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    if not cand_dir.exists():
        cand_dir.mkdir()

    outputs = solve(inputs_dir)

    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
