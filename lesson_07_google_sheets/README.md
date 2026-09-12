# Урок 7 — Google Sheets API

Записуємо зібрані дані (з уроку 5/6) напряму в Google Таблицю — так клієнту не треба відкривати CSV/Excel, дані з'являються прямо в звичному для нього інтерфейсі, і можна автоматично оновлювати їх повторно (наступний скрапінг перезапише той самий аркуш).

Налаштування Google Cloud (проєкт, Service Account, `credentials.json`, "Share" таблиці з сервісним акаунтом) вже зроблено — файл лежить в корені проєкту `credentials.json` (в `.gitignore`, не комітиться). Скрипт запускається з кореня проєкту (`python lesson_07_google_sheets/scraper.py`), тому шлях до нього — просто `"credentials.json"`, без `../`.

## Завдання

1. Прочитати `output/quotes_pandas.csv` через `pd.read_csv(...)`
2. Авторизуватись через `gspread.service_account(filename="../credentials.json")`
3. Відкрити таблицю за `SPREADSHEET_ID`
4. Записати весь DataFrame (заголовки колонок + всі рядки)
5. Вивести в консоль посилання на таблицю для перевірки

## Підказки

```python
import gspread

SPREADSHEET_ID = "1XodsIs4QirwJ5WVqe7dFBiQc7AmjclFRk5XhVVBl3jw"

gc = gspread.service_account(filename="credentials.json")
sh = gc.open_by_key(SPREADSHEET_ID)
worksheet = sh.sheet1   # перший аркуш таблиці

# заголовки + дані одним викликом
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
```

**Якщо впаде з помилкою доступу (403/PermissionError):** перевір, чи дійсно "Share" зробили саме на email з `credentials.json` (поле `client_email`), і чи права виставлені Editor, а не Viewer.

**Якщо впаде з помилкою "Google Drive API has not been used"** — Drive API ще не увімкнений в Google Cloud Console (окремо від Sheets API).

## Критерій виконання

```bash
python lesson_07_google_sheets/scraper.py
```
Відкрий саму таблицю в браузері — там мають з'явитись всі 100 цитат з колонками `text`/`author`.
