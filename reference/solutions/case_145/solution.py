import pandas as pd
from pathlib import Path
import glob


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    authors = pd.read_csv(inputs_dir / 'input_01.csv')
    awards = pd.read_csv(inputs_dir / 'input_02.csv')
    books = pd.read_csv(inputs_dir / 'input_03.csv')
    checkouts = pd.read_csv(inputs_dir / 'input_04.csv')
    book_meta = pd.read_csv(inputs_dir / 'input_05.csv')
    genre_series = pd.read_csv(inputs_dir / 'input_06.csv')
    publishers = pd.read_csv(inputs_dir / 'input_07.csv')
    ratings = pd.read_csv(inputs_dir / 'input_08.csv')
    sales_09 = pd.read_csv(inputs_dir / 'input_09.csv')
    sales_10 = pd.read_csv(inputs_dir / 'input_10.csv')
    sales_11 = pd.read_csv(inputs_dir / 'input_11.csv')
    sales_12 = pd.read_csv(inputs_dir / 'input_12.csv')
    series_dim = pd.read_csv(inputs_dir / 'input_13.csv')

    all_sales = pd.concat([sales_09, sales_10, sales_11,
                          sales_12], ignore_index=True)

    if {'BookID1', 'BookID2'}.issubset(genre_series.columns):
        genre_series['Book ID'] = genre_series['BookID1'].astype(
            str) + genre_series['BookID2'].astype(str)
    elif 'BookID' in genre_series.columns:
        genre_series['Book ID'] = genre_series['BookID']
    else:
        if 'Book ID' not in genre_series.columns:
            raise ValueError('Cannot determine Book ID in input_06.csv')

    books = books.rename(columns={'BookID': 'Book ID'})
    book_meta = book_meta.rename(columns={'BookID': 'Book ID'})
    checkouts = checkouts.rename(columns={'BookID': 'Book ID'})
    ratings = ratings.rename(columns={'BookID': 'Book ID'})

    awards_agg = awards.groupby('Title', as_index=False).agg(**{
        'Number of Awards Won (avg only)': ('Award Name', 'count')
    })

    checkouts_agg = checkouts.groupby('Book ID', as_index=False).agg(
        **{
            'Total Checkouts': ('Number of Checkouts', 'sum'),
            'Number of Months Checked Out': ('CheckoutMonth', 'nunique')
        }
    )

    ratings_agg = ratings.groupby('Book ID', as_index=False).agg(
        **{
            'Average Rating': ('Rating', 'mean'),
            'Number of Reviewers': ('ReviewerID', pd.Series.nunique),
            'Number of Reviews': ('ReviewID', 'count')
        }
    )

    df = all_sales.copy()

    df = df.merge(book_meta, on='ISBN', how='left')

    df = df.merge(books[['Book ID', 'Title', 'AuthID']],
                  on='Book ID', how='left')

    df = df.merge(authors, on='AuthID', how='left')

    df = df.merge(awards_agg, on='Title', how='left')

    df = df.merge(publishers, on='PubID', how='left')

    df = df.merge(checkouts_agg, on='Book ID', how='left')
    df = df.merge(ratings_agg, on='Book ID', how='left')

    df = df.merge(genre_series[['Book ID', 'Genre', 'SeriesID',
                  'Volume Number', 'Staff Comment']], on='Book ID', how='left')

    df = df.merge(series_dim, on='SeriesID', how='left')

    final_cols = [
        'Book ID', 'Sale Date', 'ISBN', 'Discount', 'ItemID', 'OrderID', 'First Name', 'Last Name', 'Birthday',
        'Country of Residence', 'Hrs Writing per Day', 'Title', 'AuthID', 'Format', 'PubID', 'Publication Date',
        'Pages', 'Print Run Size (k)', 'Price', 'Publishing House', 'City', 'State', 'Country', 'Year Established',
        'Marketing Spend', 'Number of Awards Won (avg only)', 'Number of Months Checked Out', 'Total Checkouts',
        'Genre', 'SeriesID', 'Volume Number', 'Staff Comment', 'Series Name', 'Planned Volumes', 'Book Tour Events',
        'Average Rating', 'Number of Reviewers', 'Number of Reviews'
    ]

    for col in final_cols:
        if col not in df.columns:
            df[col] = pd.NA

    df = df[final_cols]

    for dcol in ['Sale Date', 'Birthday', 'Publication Date']:
        dts = pd.to_datetime(df[dcol], errors='coerce')
        df[dcol] = dts.dt.strftime('%d/%m/%Y').fillna('')

    num_cols = ['Discount', 'Hrs Writing per Day', 'Price', 'Average Rating']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    int_text_cols = [
        'Pages', 'Print Run Size (k)', 'Year Established', 'Marketing Spend',
        'Number of Awards Won (avg only)', 'Number of Months Checked Out', 'Total Checkouts',
        'Volume Number', 'Planned Volumes', 'Book Tour Events', 'Number of Reviewers', 'Number of Reviews'
    ]
    for col in int_text_cols:
        if col in df.columns:
            nums = pd.to_numeric(df[col], errors='coerce').round(0)
            df[col] = nums.astype('Int64').astype('string').fillna('')

    if 'Average Rating' in df.columns:
        avg = pd.to_numeric(df['Average Rating'], errors='coerce').round(9)
        df['Average Rating'] = avg.map(lambda x: f"{x:.9f}" if pd.notna(x) else "")

    text_cols = ['Book ID', 'ISBN', 'ItemID', 'OrderID', 'First Name', 'Last Name', 'Country of Residence', 'Title', 'AuthID', 'Format',
                 'PubID', 'Publishing House', 'City', 'State', 'Country', 'Genre', 'SeriesID', 'Staff Comment', 'Series Name']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).where(
                ~df[col].isna(), '').str.strip()
            df[col] = df[col].replace({'nan': ''})

    return {'output_01.csv': df}


if __name__ == '__main__':
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'
    cand_dir = task_dir / 'cand'

    if not cand_dir.exists():
        cand_dir.mkdir()

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
