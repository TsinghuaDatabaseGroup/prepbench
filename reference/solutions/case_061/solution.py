import pandas as pd
from pathlib import Path
from itertools import product

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    transactions = {}
    all_items = set()
    
    for _, row in df.iterrows():
        trans_id = row['TransactionID']
        items_str = row['Items']
        items = [item.strip() for item in items_str.split(',')]
        transactions[trans_id] = items
        all_items.update(items)
    
    total_transactions = len(transactions)
    all_items = sorted(list(all_items))
    
    item_support = {}
    for item in all_items:
        count = sum(1 for items in transactions.values() if item in items)
        item_support[item] = count / total_transactions
    
    association_rules = []
    
    for lhs_item in all_items:
        for rhs_item in all_items:
            if lhs_item == rhs_item:
                continue
            
            both_count = sum(1 for items in transactions.values() 
                           if lhs_item in items and rhs_item in items)
            
            if both_count == 0:
                continue
            
            lhs_count = sum(1 for items in transactions.values() if lhs_item in items)
            lhs_support = lhs_count / total_transactions
            
            rhs_count = sum(1 for items in transactions.values() if rhs_item in items)
            rhs_support = rhs_count / total_transactions
            
            confidence = both_count / lhs_count if lhs_count > 0 else 0
            
            lift = confidence / rhs_support if rhs_support > 0 else 0
            
            association_rule = f"{lhs_item} --> {rhs_item}"
            
            association_rules.append({
                'AssociationRule': association_rule,
                'LHSItem': lhs_item,
                'RHSItem': rhs_item,
                'LHS Support': lhs_support,
                'RHS Support': rhs_support,
                'Confidence': confidence,
                'Lift': lift
            })
    
    output_df = pd.DataFrame(association_rules)
    
    output_df = output_df.sort_values('AssociationRule').reset_index(drop=True)
    
    return {'output_01.csv': output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

