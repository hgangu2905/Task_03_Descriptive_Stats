import os
import pandas as pd


def load_data(filepath):
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")
    return df


def analyze_overall(df):
    print("\n=== Overall Descriptive Statistics ===")
    print(df.describe(include='all'))


def analyze_categoricals(df):
    print("\n=== Top Categories (Non-Numeric Columns) ===")
    for col in df.select_dtypes(include='object').columns:
        print(f"\nColumn: {col}")
        print("  Unique values:", df[col].nunique())
        print("  Most frequent value:", df[col].mode().iloc[0] if not df[col].mode().empty else "None")


def analyze_grouped(df, group_cols, group_name="group"):
    print(f"\n=== Grouped by {', '.join(group_cols)} (showing first 3 groups) ===")
    grouped = df.groupby(group_cols)
    for i, (group_key, group_df) in enumerate(grouped):
        if i == 3:
            print("  ... (truncated)")
            break
        print(f"\nGroup: {group_name} = {group_key}")
        print(group_df.describe(include='all'))


def save_summary(df, filepath="outputs/pandas_summary.txt"):
    os.makedirs("outputs", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=== Overall Stats ===\n")
        f.write(df.describe(include='all').to_string())
        f.write("\n\n=== Categorical Columns ===\n")
        for col in df.select_dtypes(include='object').columns:
            f.write(f"\nColumn: {col}\n")
            f.write(f"  Unique values: {df[col].nunique()}\n")
            mode = df[col].mode()
            if not mode.empty:
                f.write(f"  Most frequent: {mode.iloc[0]}\n")
        f.write("\n\n=== Grouped by page_id (3 groups) ===\n")
        for i, (key, group) in enumerate(df.groupby('page_id')):
            if i == 3:
                f.write("  ... (truncated)\n")
                break
            f.write(f"\nGroup: page_id = {key}\n")
            f.write(group.describe(include='all').to_string())
        if 'ad_id' in df.columns:
            f.write("\n\n=== Grouped by page_id and ad_id (3 groups) ===\n")
            for i, (key, group) in enumerate(df.groupby(['page_id', 'ad_id'])):
                if i == 3:
                    f.write("  ... (truncated)\n")
                    break
                f.write(f"\nGroup: page_id = {key[0]}, ad_id = {key[1]}\n")
                f.write(group.describe(include='all').to_string())


if __name__ == "__main__":
    csv_file = "data/2024_fb_ads_president_scored_anon.csv"  # change for other datasets
    df = load_data(csv_file)

    analyze_overall(df)
    analyze_categoricals(df)
    analyze_grouped(df, ['page_id'], "page_id")
    if 'ad_id' in df.columns:
        analyze_grouped(df, ['page_id', 'ad_id'], "page_id,ad_id")

    save_summary(df)
    print("\n✔︎ Summary saved to outputs/pandas_summary.txt")
