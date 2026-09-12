# Урок 8 — cron / systemd timers

Налаштуємо реальний systemd timer (`--user`, без потреби в правах root), який автоматично запускає скрапер з уроку 6 кожні 2 хвилини — для навчання зроблено часто, щоб побачити результат швидко, а не чекати цілий день.

## Файли

- `scraping-practice.service` — що запускати (сам скрипт)
- `scraping-practice.timer` — коли запускати (кожні 2 хвилини + одразу через 1 хв після завантаження системи)

## Завдання

1. Скопіювати обидва файли в `~/.config/systemd/user/`
2. Перезавантажити конфігурацію systemd
3. Увімкнути і запустити timer
4. Перевірити статус і логи через `journalctl`
5. Дати попрацювати кілька хвилин, переконатись, що `output/quotes.json` оновлюється (дивись час зміни файлу)
6. **Вимкнути timer** в кінці уроку — це навчальний приклад, не має сенсу лишати його працювати вічно кожні 2 хвилини

## Команди

```bash
# 1. Скопіювати юніти
mkdir -p ~/.config/systemd/user
cp scraping-practice.service scraping-practice.timer ~/.config/systemd/user/

# 2. Перечитати конфігурацію
systemctl --user daemon-reload

# 3. Увімкнути і запустити timer
systemctl --user enable --now scraping-practice.timer

# 4. Перевірити статус
systemctl --user status scraping-practice.timer
systemctl --user list-timers   # побачити, коли наступний запуск

# логи виконання самого скрипта (після хоча б одного запуску)
journalctl --user -u scraping-practice.service -f   # -f - "стежити" в реальному часі, Ctrl+C щоб вийти

# 5. Перевірити, що файл оновлюється
ls -la /home/user/Projects/scraping-practice/output/quotes.json

# 6. Вимкнути й прибрати після завершення уроку
systemctl --user disable --now scraping-practice.timer
rm ~/.config/systemd/user/scraping-practice.service ~/.config/systemd/user/scraping-practice.timer
systemctl --user daemon-reload
```

## Підказки

**`--user` замість системного (`sudo systemctl`)** — юніт працює під твоїм користувачем, без root. На реальному VPS для продакшн-скрипта частіше роблять системний timer (`/etc/systemd/system/`, через `sudo`), але принцип той самий, і `--user` безпечніший для навчання — не чіпає нічого системного.

**Якщо timer не запускається** — перевір абсолютні шляхи в `.service` (відносні шляхи typu `python scraper.py` не працюють, systemd не знає, з якої директорії стартувати без `WorkingDirectory`).

## Критерій виконання

`systemctl --user list-timers` показує `scraping-practice.timer` з часом наступного запуску; `journalctl --user -u scraping-practice.service` показує успішні виконання без помилок.
