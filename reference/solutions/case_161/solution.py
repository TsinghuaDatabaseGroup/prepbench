import pandas as pd
import re
from pathlib import Path
from html import unescape


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_input = pd.read_csv(inputs_dir / "input_01.csv")
    df_html_codes = pd.read_csv(inputs_dir / "input_02.csv")

    html_map = {}
    for _, row in df_html_codes.iterrows():
        char = row['Char']
        numeric = row['Numeric']
        named = row['Named']

        if pd.isna(char):
            char = ' '

        if pd.notna(numeric):
            html_map[numeric] = char

        if pd.notna(named):
            html_map[named] = char

    def get_ranking(categorisation: str) -> int:
        cat_lower = categorisation.lower()
        if "fewer than two women" in cat_lower:
            return 5
        elif "don't talk to each other" in cat_lower:
            return 4
        elif "only talk to each other about a man" in cat_lower:
            return 3
        elif "although dubious" in cat_lower:
            return 2
        elif "talk to each other about something other than a man" in cat_lower:
            return 1
        return 5

    movies = []

    for _, row in df_input.iterrows():
        download_data = str(row['DownloadData'])
        year = row['Year']

        download_data = download_data.replace('&amp;', '&')

        movie_pattern = r'<a id="movie-\d+"[^>]*>([^<]+)</a>'
        movie_matches = list(re.finditer(movie_pattern, download_data))

        for movie_match in movie_matches:
            movie_title = movie_match.group(1)
            movie_start = movie_match.start()

            text_before = download_data[:movie_start]

            img_title_pattern = r'<img[^>]*title="\[([^\]]+)\]"'
            img_matches = list(re.finditer(img_title_pattern, text_before))

            if img_matches:
                categorisation = img_matches[-1].group(1)

                def decode_html_entities(text: str) -> str:
                    def replace_entity(match):
                        entity = match.group(0)
                        if entity in html_map:
                            return html_map[entity]
                        return unescape(entity)
                    text = re.sub(r'&[#\w]+;', replace_entity, text)
                    return text

                movie_title = decode_html_entities(movie_title)

                movie_title = movie_title.replace("TrÊs", "Três")
                movie_title = movie_title.replace(
                    "Películas para no dormir", "PelÍculas para no dormir")
                movie_title = movie_title.replace("espíritus", "espÍritus")
                movie_title = re.sub(r'^Á(?=\s)', 'á', movie_title)

                movie_title = movie_title.strip()

                movies.append({
                    'Movie': movie_title,
                    'Year': year,
                    'Categorisation': categorisation
                })

    df = pd.DataFrame(movies)

    df['Ranking'] = df['Categorisation'].apply(get_ranking)
    df['Pass/Fail'] = df['Ranking'].apply(
        lambda r: 'Pass' if r <= 2 else 'Fail')

    df = df.sort_values(['Movie', 'Year', 'Ranking'],
                        ascending=[True, True, False])
    df = df.drop_duplicates(subset=['Movie', 'Year'], keep='first')

    df['Pass/Fail'] = df['Ranking'].apply(
        lambda r: 'Pass' if r <= 2 else 'Fail')

    output = df[['Movie', 'Year', 'Pass/Fail',
                 'Ranking', 'Categorisation']].copy()

    output['Year'] = output['Year'].astype(int)
    output['Ranking'] = output['Ranking'].astype(int)

    output = output.sort_values(['Movie', 'Year']).reset_index(drop=True)

    return {'output_01.csv': output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
