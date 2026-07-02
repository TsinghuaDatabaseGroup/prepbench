import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_attendees = pd.read_csv(inputs_dir / "input_01.csv")
    df_am = pd.read_csv(inputs_dir / "input_02.csv")
    df_rates = pd.read_csv(inputs_dir / "input_03.csv")
    
    def extract_company(email):
        if pd.isna(email):
            return None
        domain = email.split('@')[1] if '@' in email else ''
        company = domain.split('.')[0] if '.' in domain else domain
        return company.lower() if company else None
    
    df_attendees['Company_Extracted'] = df_attendees['Email'].apply(extract_company)
    
    df_am['Company_Lower'] = df_am['Company List'].str.lower()
    
    df_merged = df_attendees.merge(
        df_am,
        left_on='Company_Extracted',
        right_on='Company_Lower',
        how='left'
    )
    
    df_merged['Company Name'] = df_merged['Company List']
    
    country_to_currency = {
        'United States': 'USD',
        'France': 'EUR',
        'Germany': 'EUR',
        'Italy': 'EUR',
        'Spain': 'EUR',
        'Canada': 'CAD',
        'Mexico': 'MXN',
        'United Kingdom': 'GBP'
    }
    
    df_merged['Currency'] = df_merged['Country'].map(country_to_currency)
    
    df_rates['Currency_Code'] = df_rates['Currency'].str.split('-').str[0]
    rates_dict = dict(zip(df_rates['Currency_Code'], df_rates['Rate']))
    
    def calculate_local_price(currency, base_price_gbp=100):
        if currency == 'GBP':
            return base_price_gbp
        rate = rates_dict.get(currency, 1)
        return int(base_price_gbp * rate)
    
    df_merged['Ticket Price Local'] = df_merged['Currency'].apply(
        lambda c: calculate_local_price(c)
    )
    
    am_client_count = df_merged.groupby('Account Manager').size().to_dict()
    df_merged['AM_Client_Count'] = df_merged['Account Manager'].map(am_client_count)
    
    df_merged = df_merged.sort_values(
        ['AM_Client_Count', 'Account Manager'],
        ascending=[False, True]
    )
    
    am_order_map = {}
    unique_ams = df_merged['Account Manager'].dropna().unique()
    sorted_ams = sorted(unique_ams, key=lambda x: am_client_count.get(x, 0), reverse=True)
    for idx, am in enumerate(sorted_ams, 1):
        am_order_map[am] = idx
    
    df_merged['Order'] = df_merged['Account Manager'].map(am_order_map)
    
    output_01 = df_merged[[
        'Order',
        'Ticket Price Local',
        'First Name',
        'Last Name',
        'Email',
        'Company Name',
        'Country',
        'Currency',
        'Refund Type',
        'Account Manager'
    ]].copy()
    
    output_01 = output_01[[
        'Order',
        'Ticket Price Local',
        'First Name',
        'Last Name',
        'Email',
        'Company Name',
        'Country',
        'Currency',
        'Refund Type',
        'Account Manager'
    ]]
    
    def calculate_gain_loss(refund_type, ticket_price):
        if refund_type == 'Full Refund':
            return -ticket_price
        elif refund_type == 'Credit Note':
            return ticket_price
        elif refund_type == 'No Refund':
            return ticket_price
        else:
            return 0
    
    df_merged['Money Gain/Loss'] = df_merged.apply(
        lambda row: calculate_gain_loss(row['Refund Type'], row['Ticket Price Local']),
        axis=1
    )
    
    output_02 = df_merged.groupby(['Country', 'Currency'])['Money Gain/Loss'].sum().reset_index()
    output_02 = output_02[[
        'Money Gain/Loss',
        'Currency',
        'Country'
    ]]
    
    output_02 = output_02.sort_values(['Money Gain/Loss', 'Currency', 'Country'], ascending=[False, True, True])
    
    return {
        "output_01.csv": output_01.reset_index(drop=True),
        "output_02.csv": output_02.reset_index(drop=True)
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

