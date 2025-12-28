Проєкт: Telegram-бот, що надсилає сповіщення про нові пригоди

Швидкий опис
- `server.py`: проста імітація сайту з ендпоїнтами для реєстрації пригод.
- `bot.py`: бот, який опитує `SITE_URL/adventures/latest` і надсилає повідомлення до Telegram при нових записах.

Встановлення
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Запуск локального імітатора (тест)
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Тестова реєстрація пригоди (curl)
```bash
curl -X POST http://localhost:8000/adventures -H "Content-Type: application/json" -d '
```

Запуск бота
1. Скопіюйте `.env.example` у `.env` та заповніть `TELEGRAM_BOT_TOKEN` і `TARGET_CHAT_ID`.
2. Для тесту поставте `SITE_URL=http://localhost:8000`.
3. Запустіть:
```bash
python bot.py
```

Примітки
- За відсутності реального API налаштовано `SITE_URL=http://XXXX` як заглушка. Помилки під час опитування очікувані для заглушки.
- Формат вхідних даних описано у `server.py` (Pydantic модель `AdventureIn`).
