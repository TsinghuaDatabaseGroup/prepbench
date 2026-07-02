import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:

    targets_df = pd.read_csv(inputs_dir / "input_01.csv")
    trans_df = pd.read_csv(inputs_dir / "input_02.csv")
    trans_df["TransactionDate"] = pd.to_datetime(trans_df["TransactionDate"])

    cutoff_this = datetime(2020, 10, 9)

    def week_day(dt: datetime):
        y = dt.year
        py = dt.weekday()
        day = ((py + 1) % 7) + 1
        jan1 = datetime(y, 1, 1)
        days_to_sun = (6 - jan1.weekday()) % 7
        first_sun = jan1 + timedelta(days=days_to_sun)
        if dt < first_sun:
            wk = 1
        else:
            wk = 2 + (dt.date() - first_sun.date()).days // 7
        return y, wk, day

    def dates_for_week(y: int, w: int):
        jan1 = datetime(y, 1, 1)
        days_to_sun = (6 - jan1.weekday()) % 7
        first_sun = jan1 + timedelta(days=days_to_sun)
        if w == 1:
            first_sat = first_sun - timedelta(days=1)
            days = (first_sat.date() - jan1.date()).days + 1
            return [jan1 + timedelta(days=i) for i in range(days)]
        else:
            start = first_sun + timedelta(days=(w - 2) * 7)
            return [start + timedelta(days=i) for i in range(7)]

    trans_df["Year"] = trans_df["TransactionDate"].dt.year
    trans_df[["Week", "Day"]] = trans_df["TransactionDate"].apply(
        lambda d: pd.Series(week_day(d)[1:3]))
    trans_df["Type"] = trans_df["Year"].map(
        {2020: "This Year", 2019: "Last Year"})
    trans_df = trans_df[trans_df["Type"].notna()].copy()

    _, cutoff_wk, cutoff_dy = week_day(cutoff_this)
    jan1_2020 = datetime(2020, 1, 1)
    days_to_sun_2020 = (6 - jan1_2020.weekday()) % 7
    fs_2020 = jan1_2020 + timedelta(days=days_to_sun_2020)
    jan1_2019 = datetime(2019, 1, 1)
    days_to_sun_2019 = (6 - jan1_2019.weekday()) % 7
    fs_2019 = jan1_2019 + timedelta(days=days_to_sun_2019)
    weeks_index = (cutoff_this.date() - fs_2020.date()).days // 7
    ly_cut_date_aligned = fs_2019 + \
        timedelta(days=weeks_index*7 + (cutoff_dy-1))

    tgt_rows = []
    for _, r in targets_df.iterrows():
        y = r["Year"]
        w = r["Week"]
        prod = r["ProductName"]
        qty_week = r["Quantity Target"]
        inc_week = r["Income Target"]
        per_day_qty = qty_week / 7.0
        per_day_inc = inc_week / 7.0
        for d in dates_for_week(y, w):
            _, wk_i, dy_i = week_day(d)
            tgt_rows.append({
                "Date": d,
                "Year": y,
                "Week": wk_i,
                "Day": dy_i,
                "ProductName": prod,
                "Quantity": per_day_qty,
                "Income": per_day_inc,
                "Type": "Target",
            })
    tgt_daily = pd.DataFrame(tgt_rows)

    def upto_anchor(df):
        return df[(df["Week"] < cutoff_wk) | ((df["Week"] == cutoff_wk) & (df["Day"] <= cutoff_dy))]

    trans_ytd = upto_anchor(trans_df)
    tgt_ytd = upto_anchor(tgt_daily)

    comb = pd.concat([
        trans_ytd.assign(Date=lambda x: x["TransactionDate"])[
            ["Date", "Year", "Week", "Day", "ProductName", "Quantity", "Income", "Type"]],
        tgt_ytd[["Date", "Year", "Week", "Day",
                 "ProductName", "Quantity", "Income", "Type"]]
    ], ignore_index=True)

    def ytd_sum_anchor(df, typ, metric, wk, dy):
        m = (df["Type"] == typ) & (
            ((df["Week"] < wk) | ((df["Week"] == wk) & (df["Day"] <= dy))))
        return df.loc[m, metric].sum()

    out = []

    for prod in comb["ProductName"].unique():
        sub = comb[comb["ProductName"] == prod]
        for metric in ["Quantity", "Income"]:
            ytd_ty = ytd_sum_anchor(
                sub, "This Year", metric, cutoff_wk, cutoff_dy)
            ytd_ly = ytd_sum_anchor(
                sub, "Last Year", metric, cutoff_wk, cutoff_dy)
            ytd_tg = ytd_sum_anchor(
                sub, "Target", metric, cutoff_wk, cutoff_dy)

            mtd_ty = sub[(sub["Type"] == "This Year") & (sub["Date"] >= datetime(
                2020, 10, 1)) & (sub["Date"] <= cutoff_this)][metric].sum()
            mtd_ly = sub[(sub["Type"] == "Last Year") & (sub["Date"] >= datetime(
                2019, 10, 1)) & (sub["Date"] <= ly_cut_date_aligned)][metric].sum()
            mtd_tg = sub[(sub["Type"] == "Target") & (sub["Date"] >= datetime(
                2020, 10, 1)) & (sub["Date"] <= cutoff_this)][metric].sum()

            def wtd_sum(typ):
                m = (sub["Type"] == typ) & (sub["Week"] ==
                                            cutoff_wk) & (sub["Day"] <= cutoff_dy)
                return sub.loc[m, metric].sum()
            wtd_ty = wtd_sum("This Year")
            wtd_ly = wtd_sum("Last Year")
            wtd_tg = wtd_sum("Target")

            def pct(a, b):
                if b == 0:
                    return 0.0
                return round((a - b) / b, 2)

            for tp, ty, ly, tg in [
                ("YTD", ytd_ty, ytd_ly, ytd_tg),
                ("MTD", mtd_ty, mtd_ly, mtd_tg),
                ("WTD", wtd_ty, wtd_ly, wtd_tg),
            ]:
                r_ty = int(round(ty))
                r_ly = int(round(ly))
                r_tg = int(round(tg))
                out.append({
                    "ProductName": prod,
                    "Metric": metric,
                    "Time Period": tp,
                    "This Year": r_ty,
                    "Last Year": r_ly,
                    "Target": r_tg,
                    "% Difference to Last Year": pct(r_ty, r_ly),
                    "% Difference to Target": pct(r_ty, r_tg),
                })

    res = pd.DataFrame(out)
    res["ProductName"] = res["ProductName"].astype(str)
    res["Metric"] = res["Metric"].astype(str)
    res["Time Period"] = res["Time Period"].astype(str)
    res["This Year"] = res["This Year"].astype(int)
    res["Last Year"] = res["Last Year"].astype(int)
    res["Target"] = res["Target"].astype(int)
    res["% Difference to Last Year"] = res["% Difference to Last Year"].astype(
        float)
    res["% Difference to Target"] = res["% Difference to Target"].astype(float)

    return {"output_01.csv": res}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
