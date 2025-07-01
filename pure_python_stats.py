import csv
import os
import sys
from collections import Counter, defaultdict
import statistics
from typing import Dict, List, Any, Tuple


# helpers

def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def load_rows(csv_path: str) -> List[dict]:
    """Read entire CSV into a list of dicts (one per row)."""
    with open(csv_path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# core statistics routine

def compute_stats(rows: List[Dict[str, str]]) -> Dict[str, Dict[str, Any]]:
    if not rows:
        return {}

    stats: Dict[str, Dict[str, Any]] = {}
    columns = rows[0].keys()

    for col in columns:
        values = [row[col] for row in rows if row[col] != ""]
        num_values = [float(v) for v in values if is_float(v)]

        col_stat = {"count": len(values)}

        if num_values:                                   # numeric column
            col_stat.update(
                mean=sum(num_values) / len(num_values),
                min=min(num_values),
                max=max(num_values),
                std_dev=statistics.stdev(num_values) if len(num_values) > 1 else 0.0,
            )
        else:                                            # categorical column
            freq = Counter(values)
            col_stat.update(
                unique_values=len(freq),
                most_common=freq.most_common(1)[0] if freq else None,
            )

        stats[col] = col_stat

    return stats


def group_rows(rows: List[dict], keys: List[str]) -> Dict[Tuple[Any, ...], List[dict]]:
    """Return a dict keyed by the tuple of `keys`, each value is the list of rows."""
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[k] for k in keys)].append(row)
    return grouped


# pretty printing 

def dump_stats(stats: Dict[str, Dict[str, Any]], indent: int = 0) -> str:
    pad = " " * indent
    lines = []
    for col, col_stats in stats.items():
        lines.append(f"{pad}• Column: {col}")
        for k, v in col_stats.items():
            lines.append(f"{pad}    {k}: {v}")
    return "\n".join(lines)


# main 

def main():
    if len(sys.argv) < 2:
        print("Usage: python pure_python_stats.py <csv_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    rows = load_rows(csv_path)
    print(f"Loaded {len(rows):,} rows from {csv_path}\n")

    os.makedirs("outputs", exist_ok=True)
    out_path = os.path.join("outputs", "pure_python_summary.txt")

    with open(out_path, "w", encoding="utf-8") as out:
        # 1) overall 
        overall = compute_stats(rows)
        print("=== Overall dataset ===")
        print(dump_stats(overall, 2))
        out.write("=== Overall dataset ===\n")
        out.write(dump_stats(overall, 2) + "\n\n")

        # 2) by page_id 
        if "page_id" in rows[0]:
            print("\n=== Grouped by page_id (showing first 5) ===")
            out.write("=== Grouped by page_id ===\n")
            for i, (pid, grp) in enumerate(group_rows(rows, ["page_id"]).items()):
                if i == 5:                       # avoid endless console spam
                    print("  ... (truncated)")
                    break
                header = f"page_id = {pid}"
                print(f"\n{header}")
                stats = compute_stats(grp)
                print(dump_stats(stats, 4))

                out.write(f"\n{header}\n")
                out.write(dump_stats(stats, 4) + "\n")

        # 3) by page_id & ad_id 
        if {"page_id", "ad_id"}.issubset(rows[0]):
            print("\n=== Grouped by (page_id, ad_id) (showing first 3) ===")
            out.write("\n=== Grouped by (page_id, ad_id) ===\n")
            for i, ((pid, aid), grp) in enumerate(group_rows(rows, ["page_id", "ad_id"]).items()):
                if i == 3:
                    print("  ... (truncated)")
                    break
                header = f"page_id = {pid} | ad_id = {aid}"
                print(f"\n{header}")
                stats = compute_stats(grp)
                print(dump_stats(stats, 4))

                out.write(f"\n{header}\n")
                out.write(dump_stats(stats, 4) + "\n")

    print(f"\n✔︎ Full results written to {out_path}")


if __name__ == "__main__":
    main()
