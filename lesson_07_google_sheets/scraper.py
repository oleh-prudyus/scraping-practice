import pandas as pd
import gspread

SOURCE_CSV = "output/quotes_pandas.csv"
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = "1XodsIs4QirwJ5WVqe7dFBiQc7AmjclFRk5XhVVBl3jw"


def main():
    df = pd.read_csv(SOURCE_CSV)

    gc = gspread.service_account(filename=CREDENTIALS_FILE)
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.sheet1
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    
    print(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")


if __name__ == "__main__":
    main()
