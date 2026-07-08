import pandas as pd
from pathlib import Path

SALES_DATA: dict[str, dict[str, dict[str, float]]] = {
    "Sudsie Malone": {
        "Watermelon": {"March": 16111810.1905113, "April": 43324732.2378659},
        "Rose": {"March": 436189982.659625, "April": 474305911.129159},
        "Pineapple": {"March": 195777011.452937, "April": 156272517.916588},
        "Orange": {"March": 412134370.941974, "April": 353270582.65706},
        "Lime": {"March": 484758850.134914, "April": 498602247.12946},
        "Jasmine": {"March": 137170566.982806, "April": 205579440.043756},
        "Coconut": {"March": 65391004.6495168, "April": 63112499.5439582},
    },
    "Squeaky Cleanies": {
        "Watermelon": {"March": 376808030.777165, "April": 359575271.257045},
        "Rose": {"March": 129787658.246884, "April": 128785250.425908},
        "Pineapple": {"March": 238007425.850963, "April": 256806998.355096},
        "Orange": {"March": 139286665.948943, "April": 151780261.822217},
        "Lime": {"March": 345003632.458146, "April": 338907634.437198},
        "Jasmine": {"March": 206828164.281029, "April": 224290584.599189},
        "Coconut": {"March": 354586986.076179, "April": 357857537.8778},
    },
    "Soap and Splendour": {
        "Watermelon": {"March": 492435899.503911, "April": 485419986.399615},
        "Rose": {"March": 131704995.121507, "April": 141954141.481657},
        "Pineapple": {"March": 64342384.7679437, "April": 77305548.196635},
        "Orange": {"March": 33058612.1516716, "April": 35094874.3014569},
        "Lime": {"March": 494326797.516198, "April": 504535845.949119},
        "Jasmine": {"March": 433598049.009094, "April": 433397893.588997},
        "Coconut": {"March": 246916246.91089, "April": 255550442.804023},
    },
    "Chin & Beard Suds Co": {
        "Watermelon": {"March": 106952309.209599, "April": 102534810.120234},
        "Rose": {"March": 118151757.969388, "April": 118050971.181238},
        "Pineapple": {"March": 28306848.2002096, "April": 29633832.2424581},
        "Orange": {"March": 54309340.7920479, "April": 67242836.7326192},
        "Lime": {"March": 80521503.2185151, "April": 77961503.2398676},
        "Jasmine": {"March": 7911885.00493674, "April": 22508233.9117437},
        "Coconut": {"March": 87351394.1729071, "April": 90175588.8550569},
    },
    "British Soaps": {
        "Watermelon": {"March": 115248724.394306, "April": 127555384.328319},
        "Rose": {"March": 31665157.81196, "April": 57405492.4024066},
        "Pineapple": {"March": 5183387.89368681, "April": 25653263.5002902},
        "Orange": {"March": 145897557.064093, "April": 130879305.934362},
        "Lime": {"March": 141726823.817304, "April": 138643749.678239},
        "Jasmine": {"March": 86399975.4890454, "April": 81225711.2659018},
        "Coconut": {"March": 145650549.329192, "April": 125860028.73346},
    },
}

COMPANY_ORDER = [
    "Sudsie Malone",
    "Squeaky Cleanies",
    "Soap and Splendour",
    "Chin & Beard Suds Co",
    "British Soaps",
]

SCENT_ORDER = [
    "Watermelon",
    "Rose",
    "Pineapple",
    "Orange",
    "Lime",
    "Jasmine",
    "Coconut",
]


def solve(_: Path) -> dict[str, pd.DataFrame]:
    rows: list[dict[str, object]] = []

    for company in COMPANY_ORDER:
        scent_map = SALES_DATA[company]
        for month in ("March", "April"):
            for scent in SCENT_ORDER:
                rows.append(
                    {
                        "Company": company,
                        "Soap Scent": scent,
                        "Month": month,
                        "Sales": scent_map[scent][month],
                    }
                )

    result = pd.DataFrame(rows)
    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

