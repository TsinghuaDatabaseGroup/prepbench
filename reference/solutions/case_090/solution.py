import pandas as pd
from pathlib import Path
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    
    sales_columns = ['Sales at Full Price', 'Sales at Half Price', 'Sales at Quarter Price']
    df_melted = df.melt(
        id_vars=['Costume', 'Country', 'Date'],
        value_vars=sales_columns,
        var_name='Discount_Type',
        value_name='Sales_Value'
    )
    
    df_melted = df_melted.dropna(subset=['Sales_Value'])
    
    df_melted['Price'] = df_melted['Discount_Type'].str.extract(r'(Full|Half|Quarter)')
    
    def extract_currency_value(sales_str):
        match = re.match(r'([A-Za-z$€£₹\s]+?)\s+([\d,]+\.?\d*)', sales_str.strip())
        if match:
            currency = match.group(1).strip()
            value = float(match.group(2).replace(',', ''))
            return currency, value
        return None, None
    
    df_melted[['Currency', 'Sales_Amount']] = df_melted['Sales_Value'].apply(
        lambda x: pd.Series(extract_currency_value(x))
    )
    
    df_melted['Sales_Amount'] = df_melted['Sales_Amount'].astype(int)
    
    def get_fiscal_year(date):
        if (date >= pd.Timestamp('2018-11-01')) and (date <= pd.Timestamp('2019-10-31')):
            return '2019 FY'
        elif (date >= pd.Timestamp('2019-11-01')) and (date <= pd.Timestamp('2020-10-27')):
            return '2020 FY'
        else:
            return None
    
    df_melted['Fiscal_Year'] = df_melted['Date'].apply(get_fiscal_year)
    
    df_melted = df_melted[df_melted['Fiscal_Year'].notna()]
    
    country_fixes = {
        'Indonsia': 'Indonesia',
        'Luxmbourg': 'Luxembourg',
        'Philippins': 'Philippines',
        'Slovnia': 'Slovenia',
    }
    
    df_melted['Country'] = df_melted['Country'].replace(country_fixes)
    
    costume_translation = {
        'Cat': 'Cat',
        'Gato': 'Cat',
        'Chat': 'Cat',
        'Katze': 'Cat',
        'Kat': 'Cat',
        'Katt': 'Cat',
        
        'Ghost': 'Ghost',
        'Geest': 'Ghost',
        'Geist': 'Ghost',
        'Geescht': 'Ghost',
        
        'Vampire': 'Vampire',
        'Vampiro': 'Vampire',
        'Vampir': 'Vampire',
        'Vampier': 'Vampire',
        'Vampiir': 'Vampire',
        'Vampyr': 'Vampire',
        
        'Pirate': 'Pirate',
        'Pirata': 'Pirate',
        'Pirat': 'Pirate',
        'Piraat': 'Pirate',
        
        'Zombie': 'Zombie',
        'Zombi': 'Zombie',
        'Zambi': 'Zombie',
        'Zumbi': 'Zombie',
        
        'Clown': 'Clown',
        'Klaun': 'Clown',
        'Kloun': 'Clown',
        'Klovn': 'Clown',
        
        'Dinosaur': 'Dinosaur',
        'Dinosaure': 'Dinosaur',
        'Dinosaurier': 'Dinosaur',
        'Dinosauro': 'Dinosaur',
        'Dinosaurus': 'Dinosaur',
        'Dinozaur': 'Dinosaur',
        
        'Devil': 'Devil',
        'Diable': 'Devil',
        'Diabel': 'Devil',
        'Diabo': 'Devil',
        'Diavolo': 'Devil',
        'Diavol': 'Devil',
        'Djevel': 'Devil',
        
        'Werewolf': 'Werewolf',
        'Werwolf': 'Werewolf',
        'Weerwolf': 'Werewolf',
    }
    
    df_melted['Costume'] = df_melted['Costume'].map(costume_translation)
    
    grouped = df_melted.groupby(
        ['Costume', 'Country', 'Currency', 'Price', 'Fiscal_Year'],
        as_index=False
    )['Sales_Amount'].sum()
    
    result = grouped.pivot_table(
        index=['Costume', 'Country', 'Currency', 'Price'],
        columns='Fiscal_Year',
        values='Sales_Amount',
        aggfunc='sum'
    ).reset_index()
    
    result.columns.name = None
    result = result.rename(columns={'2019 FY': '2019 FY Sales', '2020 FY': '2020 FY Sales'})
    
    result['2019 FY Sales'] = result['2019 FY Sales'].fillna(0).astype('Int64')
    result['2020 FY Sales'] = result['2020 FY Sales'].fillna(0).astype('Int64')
    
    result = result[['Costume', 'Country', 'Currency', 'Price', '2019 FY Sales', '2020 FY Sales']]
    
    return {'output_01.csv': result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    cand_dir.mkdir(exist_ok=True)
    
    results = solve(inputs_dir)
    
    for filename, df in results.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Saved {filename} to {output_path}")
