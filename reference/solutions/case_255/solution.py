from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:

    df = pd.read_csv(inputs_dir / "input_01.csv")

    df['Themes'] = df['Themes'].str.split(',').apply(
        lambda x: [s.strip() for s in x] if isinstance(x, list) else [])
    df = df.explode('Themes')
    df = df.rename(columns={'Themes': 'Themes Split'})

    df = df[df['Themes Split'].notna() & (df['Themes Split'] != '')]

    clean1_map = {
        "Aggregate to deduplicate": "Aggregate to Deduplicate",
        "Merge Fields": "Merge fields",
        "Date calcs": "Date Calcs",
        "Date Calc": "Date Calcs",
        "String calculations": "String Calculations",
        "Moving average": "Moving Average",
        "% of total": "% of Total",
        "Fill Down": "Fill down",
        "Date Calculation": "Date Calculations",
        "Simple join": "Simple Join",
        "Simple Joins": "Simple Join",
        "Simple joins": "Simple Join",
        "Logical calcs": "Logical Calcs",
        "Logical calc": "Logical Calcs",
        "Pivot rows to cols": "Pivot Rows to Cols",
        "Pivot Rows to cols": "Pivot Rows to Cols",
        "Left Joins": "Left Join",
        "% Difference From": "Difference From",
        "<= Join clause": ">= Join Clause",
        "<= Join Clause": ">= Join Clause",
        "Wildcard union": "Wildcard Union",
        "Full Outer Join": "Full outer join",
        "Numeric calcs": "Numeric Calcs",
        "Numeric Calc": "Numeric Calcs",
        "Non-equal join clause": "Non equal join clause",
        "Non equal Join Clause": "Non equal join clause",
        "Non-equal Join Clause": "Non equal join clause",
        "Right only Join": "Right Only Join",
        "Joins": "Join",
        "Mutliptle Join Clause": "Multiple Join Clause",
        "Multiple join clause": "Multiple Join Clause",
        "Mutliple Join Clause": "Multiple Join Clause",
        "multiple join clause": "Multiple Join Clause",
        "Clean Step Only": "Clean step only",
        "Ranks": "Rank",
        "Multiple pivot": "Multiple Pivot",
        "Mutliple Pivot": "Multiple Pivot",
        "Date Conversions": "Date Conversion",
        "Data Interpretor": "Data Interpreter",
        "Data interpreter": "Data Interpreter",
        "IF Statements": "IF statements",
        "IF Statement": "IF statements",
        "IF statement": "IF statements",
        "ID statment": "IF statements",
        "IF Statments": "IF statements",
        "Appends": "Append",
        "String calcs": "String Calcs",
        "Parameters": "Parameter",
        "Left Only Join": "Left only join",
        "Left only Join": "Left only join",
        "Aggregates": "Aggregate",
        "Aggrgegate": "Aggregate",
        "Aggrgeate": "Aggregate",
        "Splits": "Split",
        "Right Joins": "Right Join",
        "Multiple clause Join": "Multiple Clause Join",
        "Multiple clause join": "Multiple Clause Join",
        "Mutiple Clause Join": "Multiple Clause Join",
    }

    df['Themes Split'] = df['Themes Split'].replace(clean1_map)

    clean2_map = {
        "Pivot Cols": "Pivot Cols to Rows",
        "Wildcard Input": "Wildcard Union",
        "String functions": "String Calcs",
        "String Calculations": "String Calcs",
        "Scaffold": "Scaffolding",
        "Scaffolding (through all dimension combinations)": "Scaffolding",
        "Moving Calc": "Moving Calculation",
        "Moving Average": "Moving Calculation",
        ">= Join Clause": "Non Equal Join Clause",
        "Non equal join clause": "Non Equal Join Clause",
        "Non-equal Join Clause": "Non Equal Join Clause",
        "Non-equal Join Clause/Scaffolding": "Non Equal Join Clause",
        "Aggregation": "Aggregate",
        "Clean functions": "Cleaning calcs",
        "Convert Dates": "Date Calcs",
        "Create Date Field": "Date Calcs",
        "Date Calculations": "Date Calcs",
        "Date Conversion": "Date Calcs",
        "Date Functions": "Date Calcs",
        "Date Part": "Date Calcs",
        "Date Time Conversion": "Date Calcs",
        "Make Date": "Date Calcs",
        "Filling in blanks": "Fill down",
        "Fill down 2 fields": "Fill down",
        "Filter Duplicates": "Filters",
        "Filtering": "Filters",
        "Multi Clause Join": "Multiple Join Clause",
        "Multiple Clause Join": "Multiple Join Clause",
        "Join Practice": "Join",
        "Simple Join": "Join",
        "Right Join": "Left Join",
        "Right Only Join": "Left only join",
        "Lookup (but circular)": "Lookup",
        "Mathematical Calculations": "Numeric Calcs",
        "Merge": "Merge fields",
        "Multiple parameters": "Parameter",
        "Parameter in Output Name": "Parameter",
        "Parameter to Name Output": "Parameter",
        "Using Parameter in Output name": "Parameter",
        "Running Sum": "Running Total",
        "Updating a workflow": "Update a workflow",
        "Rename Values": "Group Values",
    }

    df['Themes Split'] = df['Themes Split'].replace(clean2_map)

    agg_df = df.groupby(['Themes Split', 'Level']).size(
    ).reset_index(name='Number of Challenges')

    pivot_df = agg_df.pivot_table(
        index='Themes Split',
        columns='Level',
        values='Number of Challenges'
    ).reset_index()

    required_levels = ['Beginner', 'Intermediate', 'Advanced', '3-in-1']
    for level in required_levels:
        if level not in pivot_df.columns:
            pivot_df[level] = pd.NA

    pivot_df['Total'] = (
        pivot_df.get('3-in-1', pd.Series([0] * len(pivot_df))).fillna(0) +
        pivot_df.get('Beginner', pd.Series([0] * len(pivot_df))).fillna(0) +
        pivot_df.get('Intermediate', pd.Series([0] * len(pivot_df))).fillna(0) +
        pivot_df.get('Advanced', pd.Series([0] * len(pivot_df))).fillna(0)
    ).astype(int)

    pivot_df['Priority'] = pivot_df['Total'].rank(
        method='dense', ascending=True).astype(int)

    pivot_df = pivot_df.rename(columns={'Themes Split': 'Technique'})

    output_columns = ['Priority', 'Technique', 'Beginner',
                      'Intermediate', 'Advanced', '3-in-1', 'Total']
    result_df = pivot_df[output_columns].copy()

    result_df = result_df.sort_values('Priority').reset_index(drop=True)

    return {"output_01.csv": result_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
