# Урок 9 — Docker-контейнер для скрипта

`Dockerfile` і `.dockerignore` лежать у **корені проєкту** (не в цій папці) — Docker будує образ з контексту всього проєкту, тому файл має бачити `requirements.txt` і всі уроки.

## Завдання

1. Зібрати образ
2. Запустити контейнер без volume — переконатись, що дані "зникають" після завершення
3. Запустити знову з volume — переконатись, що `output/` з'являється на хості
4. Порівняти розмір образу (`docker images`) — Playwright з Chromium важить чимало

## Команди

```bash
cd /home/user/Projects/scraping-practice

# 1. Зібрати образ (перший раз довго - завантажує Python, Chromium)
docker build -t scraping-practice .

# 2. Запустити БЕЗ volume
docker run --rm scraping-practice
# ОЧІКУВАНО впаде з FileNotFoundError: output/ в .dockerignore, тому quotes_pandas.csv
# (вхідні дані з уроку 5) взагалі не потрапив в образ - нема звідки читати

# 3. Запустити З volume
docker run --rm -v $(pwd)/output:/app/output scraping-practice
ls -la output/quotes.json   # тепер файл є

# 4. Розмір образу
docker images scraping-practice
```

## Підказки

**`.dockerignore`** працює як `.gitignore`, але для Docker build — файли звідти не потрапляють у контекст збірки (не копіюються в образ). Вже налаштовано: `.venv/`, `output/`, `credentials.json` не потраплять у образ (і не мають — секрет і локальне середовище там не потрібні).

**Якщо `docker build` падає на `playwright install --with-deps`** — переконайся, що в системі достатньо місця на диску (Chromium + залежності важать кілька сотень MB).

**Якщо `docker` команда взагалі не знайдена** — Docker daemon має бути встановлений і запущений (`systemctl status docker`); якщо ти вже проходив [[Docker]] раніше — має бути готово.

## Критерій виконання

`docker run --rm -v $(pwd)/output:/app/output scraping-practice` завершується без помилок, `output/quotes.json` з'являється/оновлюється на хості.
