# Task_03_Descriptive_Stats

## 🧠 Overview

This project explores advertising and social media activity related to the 2024 U.S. Presidential Election using three datasets (Facebook ads, Facebook posts, Twitter posts). The goal is to build a system that produces descriptive statistics using three different strategies:

- **Pure Python** (standard library only)
- **Pandas**
- **Polars**

All approaches generate the **same numerical results**, and include:
- Overall summary statistics
- Grouped analysis by `page_id`
- Grouped analysis by (`page_id`, `ad_id`)

Optional visualizations are also included for exploratory data analysis.

---

## ▶️ How to Run

1. **Place the dataset** (e.g., `2024_fb_ads_president_scored_anon.csv`) inside the `data/` folder.
2. Run each script using Python 3:

```bash
python pure_python_stats.py
python pandas_stats.py
python polars_stats.py
python visuals.py
