import os
import polars as pl


# helpers 
def load_data(path: str) -> pl.DataFrame:
    df = pl.read_csv(path)
    print(f"Loaded {df.height:,} rows • {df.width} columns")
    return df


def print_overall(df: pl.DataFrame) -> None:
    print("\n=== Overall Descriptive Statistics ===")
    print(df.describe())


def print_grouped(
    df: pl.DataFrame, group_cols: list[str], label: str, show_groups: int = 3
) -> None:
    print(f"\n=== Grouped by {', '.join(group_cols)} (first {show_groups} groups) ===")

    # Get first N unique combinations of the grouping columns
    sample_keys = (
        df.select(group_cols).unique(maintain_order=True).head(show_groups).iter_rows()
    )

    for key in sample_keys:
        # Build a boolean expression: (col1 == key1) & (col2 == key2) & ...
        expr = None
        for col, val in zip(group_cols, key):
            col_expr = pl.col(col) == val
            expr = col_expr if expr is None else expr & col_expr

        subgroup = df.filter(expr)
        print(f"\nGroup {label} = {key}")
        print(subgroup.describe())


def save_summary(df: pl.DataFrame, out_path: str = "outputs/polars_summary.txt") -> None:
    os.makedirs("outputs", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        # Overall stats
        f.write("=== Overall Descriptive Statistics ===\n")
        f.write(str(df.describe()))

        # Grouped by page_id
        if "page_id" in df.columns:
            f.write("\n\n=== Grouped by page_id (first 3 groups) ===\n")
            for pid, *_ in df.select("page_id").unique().head(3).iter_rows():
                pid_df = df.filter(pl.col("page_id") == pid)
                f.write(f"\npage_id = {pid}\n")
                f.write(str(pid_df.describe()))

        # Grouped by page_id + ad_id
        if {"page_id", "ad_id"}.issubset(df.columns):
            f.write("\n\n=== Grouped by (page_id, ad_id) (first 3 groups) ===\n")
            pairs = df.select(["page_id", "ad_id"]).unique().head(3).iter_rows()
            for pid, aid in pairs:
                pair_df = df.filter(
                    (pl.col("page_id") == pid) & (pl.col("ad_id") == aid)
                )
                f.write(f"\npage_id = {pid}, ad_id = {aid}\n")
                f.write(str(pair_df.describe()))


# main
if __name__ == "__main__":
    csv_file = "data/2024_fb_ads_president_scored_anon.csv"  # change for other datasets
    df = load_data(csv_file)

    print_overall(df)

    if "page_id" in df.columns:
        print_grouped(df, ["page_id"], "page_id")

    if {"page_id", "ad_id"}.issubset(df.columns):
        print_grouped(df, ["page_id", "ad_id"], "page_id, ad_id")

    save_summary(df)
    print("\n✔︎ Full summary saved to outputs/polars_summary.txt")
