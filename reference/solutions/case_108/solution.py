import pandas as pd
from pathlib import Path
import re
from decimal import Decimal, ROUND_HALF_UP


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    area_lookup = pd.read_csv(inputs_dir / "input_01.csv")
    ids_raw = pd.read_csv(inputs_dir / "input_02.csv")
    product_lookup = pd.read_csv(inputs_dir / "input_03.csv")

    def to_pence(price_str: str) -> int:
        s = str(price_str).replace('£', '').strip()
        return int((Decimal(s) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    product_lookup['Price_Pence'] = product_lookup['Price'].apply(to_pence)

    ids_series = ids_raw['IDs'].dropna().astype(str)
    split_ids = ids_series.apply(lambda s: s.strip().split())
    ids_list = [item for sub in split_ids for item in sub]
    ids_df = pd.DataFrame({'id_str': ids_list})

    def parse_id_string(id_str: str):
        phone_match = re.search(r"(\d{6})", id_str)
        after_comma = None
        m = re.search(r",(\d{2})([A-Za-z])(\d+)-([A-Za-z]+)$", id_str)
        if m:
            area_code_suffix = m.group(1)
            area_initial = m.group(2).upper()
            quantity = int(m.group(3))
            product_id = m.group(4).upper()
        else:
            area_code_suffix = None
            area_initial = None
            quantity = None
            product_id = None
        phone = phone_match.group(1) if phone_match else None
        return pd.Series({
            'Phone Number': phone,
            'Area Code Suffix': area_code_suffix,
            'Area Initial': area_initial,
            'Quantity': quantity,
            'Product ID': product_id,
        })

    parsed = ids_df['id_str'].apply(parse_id_string)
    parsed = parsed.dropna(subset=[
                           'Phone Number', 'Area Code Suffix', 'Area Initial', 'Quantity', 'Product ID'])

    area_lookup = area_lookup.copy()
    area_lookup['Area Code Suffix'] = area_lookup['Code'].astype(str).str[-2:]
    area_lookup['Area Initial'] = area_lookup['Area'].astype(
        str).str[0].str.upper()

    excluded_areas = {'Clevedon', 'Fakenham', 'Stornoway'}
    area_lookup = area_lookup[~area_lookup['Area'].isin(excluded_areas)]

    merged = parsed.merge(
        area_lookup[['Area', 'Area Code Suffix', 'Area Initial']],
        on=['Area Code Suffix', 'Area Initial'],
        how='inner'
    )

    phone_counts = merged.groupby('Phone Number').size()
    ambiguous_phones = set(phone_counts[phone_counts > 1].index)
    merged = merged[~merged['Phone Number'].isin(ambiguous_phones)]

    merged = merged.merge(product_lookup[[
                          'Product ID', 'Product Name', 'Price_Pence']], on='Product ID', how='inner')
    merged['Revenue_Pence'] = merged['Quantity'] * merged['Price_Pence']

    agg_raw = (
        merged.groupby(['Area', 'Product Name'], as_index=False)
        .agg(rev_pence=('Revenue_Pence', 'sum'))
    )

    def round_half_up_0(x: Decimal) -> int:
        return int((x).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    agg_raw['rev_pounds'] = agg_raw['rev_pence'].apply(
        lambda v: Decimal(v) / Decimal(100))
    agg_raw['Revenue'] = agg_raw['rev_pounds'].apply(round_half_up_0)

    agg_raw['Rank'] = agg_raw.groupby('Area')['Revenue'].rank(
        method='min', ascending=False).astype(int)

    total_rev_int = agg_raw.groupby('Area')['Revenue'].transform('sum')

    def pct_half_up_int(value: int, total: int) -> float:
        if total == 0:
            return 0.0
        pct = (Decimal(value) / Decimal(total)) * Decimal(100)
        return float(pct.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    agg_raw['% of Total - Product'] = [
        pct_half_up_int(int(v), int(t)) for v, t in zip(agg_raw['Revenue'], total_rev_int)
    ]

    out = agg_raw[['Rank', 'Area', 'Product Name',
                   'Revenue', '% of Total - Product']]

    out = out.sort_values(['Area', 'Rank', 'Product Name']
                          ).reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    results = solve(inputs_dir)

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    for filename, df in results.items():
        (cand_dir / filename).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
