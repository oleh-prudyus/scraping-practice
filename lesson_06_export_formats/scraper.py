import os
import sqlite3

import pandas as pd

SOURCE_CSV = "output/quotes_pandas.csv"


def main():
    os.makedirs("output", exist_ok=True)
    df = pd.read_csv(SOURCE_CSV)
    
    df.to_json("output/quotes.json", orient="records", force_ascii=False, indent=2)
    df.to_excel("output/quotes.xlsx", index=False)

    conn = sqlite3.connect("output/quotes.db")
    df.to_sql("quotes",conn,if_exists="replace", index=False)
    
    result = pd.read_sql("SELECT COUNT(*) as cnt FROM quotes", conn)
    print(result)
    conn.close()
    
if __name__ == "__main__":
    main()
