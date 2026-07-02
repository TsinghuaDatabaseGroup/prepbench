import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_country_codes = pd.read_csv(inputs_dir / "input_01.csv")
    df_hosts = pd.read_csv(inputs_dir / "input_02.csv")
    df_medals = pd.read_csv(inputs_dir / "input_03.csv")

    # Fill NaN values
    df_medals['Country Code'] = df_medals['Country Code'].fillna('')
    df_medals['Country'] = df_medals['Country'].fillna('')
    _orig_country = df_medals['Country'].copy()

    # Fix Great Britain naming
    df_medals['Country'] = df_medals['Country'].replace(
        'Great Britain at the 2012 Summer Olympics', 'Great Britain')

    # Create lookup dictionaries
    code_to_country = dict(zip(df_country_codes['Code'], df_country_codes['Country']))
    country_to_code = dict(zip(df_country_codes['Country'], df_country_codes['Code']))

    # Fill Country from Code
    df_medals['Country'] = df_medals.apply(
        lambda row: code_to_country.get(row['Country Code'], row['Country'])
        if not row['Country'] else row['Country'], axis=1)

    # Fill Code from Country
    df_medals['Country Code'] = df_medals.apply(
        lambda row: country_to_code.get(row['Country'], row['Country Code'])
        if not row['Country Code'] else row['Country Code'], axis=1)

    # Filter out Great Britain 2012 entries and empty entries
    df_medals = df_medals[_orig_country != 'Great Britain at the 2012 Summer Olympics'].copy()
    df_medals = df_medals[(df_medals['Country'] != '') & (df_medals['Country Code'] != '')].copy()

    # Sport normalization
    df_medals['Sport'] = df_medals['Sport'].replace({'Canoeing': 'Canoe / Kayak', 'Swimming': 'Aquatics'})

    # Event normalization - metres/km
    df_medals['Event'] = df_medals['Event'].str.replace(
        r'\b(metre|metres)\b', 'm', regex=True, case=False).str.replace(
        r'\bkilometres\b|(\d+)kilometres\b', lambda m: f'{m.group(1)}km' if m.group(1) else 'km', regex=True, case=False).str.replace(
        r'(\d+)\s*km\b', r'\1 km', regex=True).str.replace(
        r'(\d+\.\d+)\s*km\b', r'\1km', regex=True)

    # Cycling km normalization
    is_cycling = df_medals['Sport'] == 'Cycling'
    df_medals.loc[is_cycling, 'Event'] = df_medals.loc[is_cycling, 'Event'].str.replace(
        r'\b(?!25\b)(\d+)\s+km\b', r'\1km', regex=True)

    # Diving m normalization
    is_diving = df_medals['Sport'] == 'Diving'
    df_medals.loc[is_diving, 'Event'] = df_medals.loc[is_diving, 'Event'].str.replace(
        r'\b(\d+)\s*m\s+(springboard|platform)\b', r'\1 m \2', regex=True)

    # Shooting m normalization
    is_shooting = df_medals['Sport'] == 'Shooting'

    # Air pistol/rifle with shots
    mask_air_shots = is_shooting & df_medals['Event'].str.contains(
        r'air\s+(pistol|rifle)', case=False, regex=True, na=False) & df_medals['Event'].str.contains('\\(.*shots\\)', case=False, na=False)
    df_medals.loc[mask_air_shots, 'Event'] = df_medals.loc[mask_air_shots, 'Event'].str.replace(
        r'(\b\d+)\s*m\b', r'\1m', regex=True)

    # Air pistol/rifle without shots
    mask_air_no_shots = is_shooting & df_medals['Event'].str.contains(
        r'air\s+(pistol|rifle)', case=False, regex=True, na=False) & ~df_medals['Event'].str.contains('\\(.*shots\\)', case=False, na=False)
    df_medals.loc[mask_air_no_shots, 'Event'] = df_medals.loc[mask_air_no_shots, 'Event'].str.replace(
        r'(\b\d+)\s*m\b', r'\1 m', regex=True)

    # Rapid fire pistol without shots
    mask_rfp_no_shots = is_shooting & df_medals['Event'].str.contains(
        'rapid fire pistol', case=False, na=False) & ~df_medals['Event'].str.contains('\\(.*shots\\)', case=False, na=False)
    df_medals.loc[mask_rfp_no_shots, 'Event'] = df_medals.loc[mask_rfp_no_shots, 'Event'].str.replace(
        r'(\b\d+)\s*m(\s+rapid)', r'\1 m\2', regex=True)

    # Army, small bore/small/free rifle - no space
    mask_no_space = is_shooting & (df_medals['Event'].str.contains('army', case=False, na=False) |
                                    df_medals['Event'].str.contains('small bore rifle|small rifle|free rifle', case=False, na=False))
    df_medals.loc[mask_no_space, 'Event'] = df_medals.loc[mask_no_space, 'Event'].str.replace(
        r'(\b\d+)\s*m\b', r'\1m', regex=True)

    # General pistol/rifle - with space
    mask_exclude = df_medals['Event'].str.contains(
        r'air\s+(pistol|rifle)|rapid fire pistol|army|small bore rifle|small rifle|free rifle|\(.*shots\)', case=False, regex=True, na=False)
    mask_general_space = is_shooting & df_medals['Event'].str.contains(
        r'\b(pistol|rifle)\b', case=False, regex=True, na=False) & ~mask_exclude
    df_medals.loc[mask_general_space, 'Event'] = df_medals.loc[mask_general_space, 'Event'].str.replace(
        r'(\b\d+)\s*m\b', r'\1 m', regex=True)

    # Athletics walk events
    df_medals['Event'] = df_medals['Event'].str.replace(
        r'\b(50|20)\s+km\s+(race\s+)?walk\b', lambda m: f'{m.group(1)}km {m.group(2) or ""}walk', regex=True).str.replace(
        r'\bmarathon\s+10\s+km\b', 'marathon 10km', regex=True)

    df_medals.loc[(df_medals['Year'] == 2016) & (df_medals['Sport'] == 'Athletics') &
                  df_medals['Event'].str.contains(r'^(20|50)km walk$', regex=True), 'Event'] = \
        df_medals.loc[(df_medals['Year'] == 2016) & (df_medals['Sport'] == 'Athletics') &
                      df_medals['Event'].str.contains(r'^(20|50)km walk$', regex=True), 'Event'].str.replace(
        r'^(\d+)km walk$', r'\1 km walk', regex=True)

    # Canoe/Kayak m normalization
    is_ck = df_medals['Sport'] == 'Canoe / Kayak'
    df_medals.loc[is_ck, 'Event'] = df_medals.loc[is_ck, 'Event'].str.replace(
        r'(\b[CK]-\d\s+\d{3,4})m\b(?!\s*\()', r'\1 m', regex=True)

    # Swimming normalization
    is_swimming = (df_medals['Sport'] == 'Aquatics') & (df_medals['Discipline'].str.contains('Swimming', na=False))

    # Swimming relay
    relay_mask = is_swimming & df_medals['Event'].str.contains(r'\bx\b', case=False, regex=True, na=False)
    df_medals.loc[relay_mask, 'Event'] = df_medals.loc[relay_mask, 'Event'].str.replace(
        r'\b(\d+)\s*x\s*(\d{2,4})\s*m\b', r'\1 x \2 m', regex=True)

    # Swimming non-relay
    non_relay = is_swimming & ~relay_mask
    df_medals.loc[non_relay & (df_medals['Year'] >= 2012), 'Event'] = df_medals.loc[non_relay & (df_medals['Year'] >= 2012), 'Event'].str.replace(
        r'(\b\d{2,4})m\b', r'\1 m', regex=True)
    df_medals.loc[non_relay & (df_medals['Year'] < 2012), 'Event'] = df_medals.loc[non_relay & (df_medals['Year'] < 2012), 'Event'].str.replace(
        r'(\b\d{2,4})\s+m\b', r'\1m', regex=True)

    # Open water and marathon
    df_medals.loc[is_swimming & df_medals['Event'].str.contains('open water|marathon', case=False, regex=True, na=False), 'Event'] = \
        df_medals.loc[is_swimming & df_medals['Event'].str.contains('open water|marathon', case=False, regex=True, na=False), 'Event'].str.replace(
            r'(\b\d+)\s+km(\s+marathon)?\b', r'\1km\2', regex=True)

    # Athletics relay normalization
    is_ath = (df_medals['Sport'] == 'Athletics') & (df_medals['Discipline'].str.contains('Athletics', na=False))
    relay_mask_ath = is_ath & df_medals['Event'].str.contains(r'[x×]', na=False) & df_medals['Event'].str.contains(r'relay', case=False, na=False)
    df_medals.loc[relay_mask_ath, 'Event'] = df_medals.loc[relay_mask_ath, 'Event'].str.replace(
        r'(\b\d+)\s*[x×]\s*(\d{2,4})\s*m\b', r'\1x\2m', regex=True)

    # Gender-specific relay x/× normalization
    mask_women_2012p = relay_mask_ath & (df_medals['Event_Gender'] == 'W') & (df_medals['Year'] >= 2012)
    mask_women_pre2012 = relay_mask_ath & (df_medals['Event_Gender'] == 'W') & (df_medals['Year'] < 2012)
    mask_men_2016p = relay_mask_ath & (df_medals['Event_Gender'] == 'M') & (df_medals['Year'] >= 2016)
    mask_men_pre2016 = relay_mask_ath & (df_medals['Event_Gender'] == 'M') & (df_medals['Year'] < 2016)

    df_medals.loc[mask_women_2012p, 'Event'] = df_medals.loc[mask_women_2012p, 'Event'].str.replace('x', '×', regex=False)
    df_medals.loc[mask_women_pre2012, 'Event'] = df_medals.loc[mask_women_pre2012, 'Event'].str.replace('×', 'x', regex=False)
    df_medals.loc[mask_men_2016p, 'Event'] = df_medals.loc[mask_men_2016p, 'Event'].str.replace('x', '×', regex=False)
    df_medals.loc[mask_men_pre2016, 'Event'] = df_medals.loc[mask_men_pre2016, 'Event'].str.replace('×', 'x', regex=False)

    # Athletics non-relay
    df_medals.loc[is_ath & ~relay_mask_ath, 'Event'] = df_medals.loc[is_ath & ~relay_mask_ath, 'Event'].str.replace(
        r'(\b\d{2,4})\s+m\b', r'\1m', regex=True)

    # Discipline normalization
    df_medals.loc[(df_medals['Sport'] == 'Cycling') & (df_medals['Year'] == 1896) &
                  (df_medals['Event'].str.lower() == 'individual road race'), 'Discipline'] = 'Cycling Track'

    df_medals['Discipline'] = df_medals['Discipline'].replace({
        'Wrestling Gre-R': 'Greco-Roman', 'Gre-Roman': 'Greco-Roman',
        'Modern Pentathalon ': 'Modern Pentathalon', 'Modern Pentath.': 'Modern Pentathalon',
        'Modern Pentath': 'Modern Pentathalon', 'Modern pentathlon': 'Modern Pentathalon',
        'Synchronized S.': 'Synchronized Swimming', 'Synchronized swimming': 'Synchronized Swimming',
        'synchronized swimming': 'Synchronized Swimming', 'Beach volley.': 'Beach volleyball',
        'Mountain biking': 'Mountain Bike', 'Artistic': 'Artistic G.', 'Artistic Gymnastics': 'Artistic G.',
        'Rhythmic': 'Rhythmic G.', 'Rhythmic Gymnastics': 'Rhythmic G.'
    })

    # Cycling Track normalization
    cycling_mask = df_medals['Sport'] == 'Cycling'
    track_conditions = (
        df_medals['Discipline'].str.lower().str.contains('track cycling|cycling track|road cycling|cycling road', na=False) |
        (df_medals['Year'] <= 1992) |
        df_medals['Event'].str.lower().str.contains('road race|time trial', na=False)
    )
    df_medals.loc[cycling_mask & track_conditions, 'Discipline'] = 'Cycling Track'

    # Synchronized Swimming normalization
    df_medals.loc[df_medals['Discipline'].astype(str).str.contains('Synchronized', case=False, na=False), 'Discipline'] = 'Synchronized Swimming'

    # Output 03
    df_output03 = df_medals[['Country', 'Country Code', 'Sport', 'Medal', 'Event',
                             'Athlete', 'Year', 'Event_Gender', 'Discipline']].copy()
    df_output03.columns = ['Country', 'Code', 'Sport', 'Medal', 'Event',
                           'Athlete', 'Year', 'Event_Gender', 'Discipline']
    df_output03 = df_output03.drop_duplicates()

    medal_order = {'Gold': 0, 'Silver': 1, 'Bronze': 2}
    gender_order = {'M': 0, 'W': 1}
    df_output03['_medal_order'] = df_output03['Medal'].map(medal_order)
    df_output03['_gender_order'] = df_output03['Event_Gender'].map(gender_order)
    df_output03 = df_output03.sort_values(
        by=['Year', 'Sport', 'Event', '_medal_order', '_gender_order', 'Country']
    ).drop(columns=['_medal_order', '_gender_order']).reset_index(drop=True)

    # Output 01 - Medal counts
    df_medals_for_agg = df_medals.copy()
    is_ck = df_medals_for_agg['Sport'] == 'Canoe / Kayak'
    df_ck = df_medals_for_agg[is_ck].drop_duplicates(
        subset=['Country', 'Year', 'Medal', 'Event', 'Sport', 'Event_Gender'])
    df_non_ck = df_medals_for_agg[~is_ck].drop_duplicates(
        subset=['Country', 'Year', 'Medal', 'Event', 'Sport', 'Event_Gender', 'Discipline'])

    df_medals_unique = pd.concat([df_ck, df_non_ck], ignore_index=True)
    df_medals_agg = df_medals_unique.groupby(['Country', 'Year', 'Medal']).size().reset_index(name='Count')

    df_pivot = df_medals_agg.pivot_table(index=['Country', 'Year'], columns='Medal', values='Count').reset_index()
    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in df_pivot.columns:
            df_pivot[medal] = pd.NA

    df_output01 = df_pivot[['Country', 'Gold', 'Silver', 'Bronze', 'Year']].copy()
    for col in ['Gold', 'Silver', 'Bronze']:
        df_output01[col] = df_output01[col].apply(lambda x: '' if pd.isna(x) else int(x))

    df_output01 = df_output01.sort_values(by=['Year', 'Country'], ascending=[False, True]).reset_index(drop=True)

    # Output 02 - Host cities
    df_output02 = df_hosts.copy()

    host_info = df_output02['Host'].str.strip('"').str.strip().str.replace('\xa0', ' ').str.split(',', n=1, expand=True)
    df_output02['Host City'] = host_info[0].str.strip()
    df_output02['Host Country'] = host_info[1].str.strip() if 1 in host_info.columns else ''
    df_output02['Host Country'] = df_output02['Host Country'].replace('United Kingdom', 'Great Britain')

    # Date normalization
    def norm_date(s: str) -> str:
        if pd.isna(s) or s == '':
            return ''
        s = str(s)
        if '-' in s:
            try:
                y, a, b = s.split(' ')[0].split('-')
                if len(y) == 4 and len(a) == 2 and len(b) == 2:
                    return f'{int(a):02d}/{int(b):02d}/{int(y):04d}'
            except Exception:
                pass
            dt = pd.to_datetime(s, errors='coerce')
            return dt.strftime('%d/%m/%Y') if pd.notna(dt) else ''
        parts = s.split('/')
        if len(parts) == 3:
            try:
                m, d, y = int(parts[0]), int(parts[1]), int(parts[2])
                dt = pd.to_datetime(
                    f'{m:02d}/{d:02d}/{y:04d}', format='%m/%d/%Y', errors='coerce')
                if pd.notna(dt):
                    return dt.strftime('%d/%m/%Y')
            except Exception:
                pass
            try:
                d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                dt = pd.to_datetime(
                    f'{d:02d}/{m:02d}/{y:04d}', format='%d/%m/%Y', errors='coerce')
                if pd.notna(dt):
                    return dt.strftime('%d/%m/%Y')
            except Exception:
                pass
        dt = pd.to_datetime(s, errors='coerce')
        return dt.strftime('%d/%m/%Y') if pd.notna(dt) else ''

    df_output02['Start Date'] = df_output02['Start Date'].apply(norm_date)
    df_output02['End Date'] = df_output02['End Date'].apply(norm_date)
    df_output02['Year'] = df_output02['Start Date'].str.split('/').str[-1].astype(int, errors='ignore')

    df_output02 = df_output02[['Year', 'Host City', 'Host Country', 'Start Date', 'End Date',
                               'Games', 'Nations', 'Sports', 'Events']].copy()
    df_output02 = df_output02.sort_values(by='Year').reset_index(drop=True)

    return {
        'output_01.csv': df_output01,
        'output_02.csv': df_output02,
        'output_03.csv': df_output03
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
