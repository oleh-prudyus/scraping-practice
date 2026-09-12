# Урок 6 — Експорт у JSON, Excel, SQLite

Той самий DataFrame з уроку 5 — тепер збережи його одразу в кількох форматах, які реально просять клієнти на фрілансі (не всі хочуть CSV).

## Завдання

1. Прочитати `output/quotes_pandas.csv` (результат уроку 5) через `pd.read_csv(...)`
2. Зберегти в JSON: `output/quotes.json`
3. Зберегти в Excel: `output/quotes.xlsx`
4. Зберегти в SQLite: таблиця `quotes` у файлі `output/quotes.db`
5. Перевірити SQLite — прочитати назад через SQL-запит і вивести кількість рядків

## Підказки

**JSON:**
```python
df.to_json("output/quotes.json", orient="records", force_ascii=False, indent=2)
```
- `orient="records"` — список об'єктів `[{...}, {...}]`
- `force_ascii=False` — щоб текст не перетворювався на `\uXXXX`

**Excel** (потрібен `openpyxl`, вже доданий в requirements.txt):
```python
df.to_excel("output/quotes.xlsx", index=False)
```

**SQLite:**
```python
import sqlite3

conn = sqlite3.connect("output/quotes.db")
df.to_sql("quotes", conn, if_exists="replace", index=False)

# перевірка - прочитати назад
result = pd.read_sql("SELECT COUNT(*) as cnt FROM quotes", conn)
print(result)

conn.close()
```

## Критерій виконання

```bash
python lesson_06_export_formats/scraper.py
```
Створює `output/quotes.json`, `output/quotes.xlsx`, `output/quotes.db`. У консолі — підтвердження кількості рядків у SQLite (має бути 100).
