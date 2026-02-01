#!/usr/bin/env python3
"""
Preview sample data from dashboard.db. Run: python preview_dashboard_db.py
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "dashboard.db"


def main():
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        print("Run: python seed_dashboard_db.py")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    for table in tables:
        cur.execute(f"SELECT * FROM [{table}] LIMIT 10")
        rows = cur.fetchall()
        if not rows:
            print(f"\n--- {table} (0 rows) ---\n")
            continue
        cols = list(rows[0].keys())
        print(f"\n--- {table} (sample, up to 10 rows) ---")
        print("  " + " | ".join(cols))
        print("  " + "-" * (sum(len(c) for c in cols) + 3 * (len(cols) - 1)))
        for row in rows:
            print("  " + " | ".join(str(row[c])[:20] for c in cols))
        cur.execute(f"SELECT COUNT(*) FROM [{table}]")
        n = cur.fetchone()[0]
        if n > 10:
            print(f"  ... and {n - 10} more rows (total {n})")
    conn.close()
    print()


if __name__ == "__main__":
    main()
