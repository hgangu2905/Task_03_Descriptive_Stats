import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the dataset
csv_path = "data/2024_fb_ads_president_scored_anon.csv"
df = pd.read_csv(csv_path)

# Make output folder
os.makedirs("outputs/visuals", exist_ok=True)

# Histogram of ad spend
if "spend" in df.columns:
    plt.figure(figsize=(8, 5))
    sns.histplot(df["spend"].dropna(), bins=30, kde=True)
    plt.title("Distribution of Ad Spend")
    plt.xlabel("Spend ($)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("outputs/visuals/spend_histogram.png")
    plt.close()

# Bar chart of top 10 most active pages
if "page_id" in df.columns:
    top_pages = df["page_id"].value_counts().nlargest(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_pages.index.astype(str), y=top_pages.values)
    plt.title("Top 10 Pages by Ad Count")
    plt.xlabel("Page ID")
    plt.ylabel("Number of Ads")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/visuals/top_pages_bar.png")
    plt.close()

print("✔︎ Visualizations saved to outputs/visuals/")
