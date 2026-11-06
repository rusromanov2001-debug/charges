# Трекер чарджей

Красивый веб-трекер для учёта чарджей с кнопкой «Вернули / Не вернули».

## Возможности
- Добавление чарджей (сумма, дата, токен, номер, сколько вернули)
- Таблица со всеми полями
- Кнопка переключения статуса «Вернули» / «Не вернули»
- Удаление записей
- Тёмная современная тема
- Данные сохраняются в SQLite

## Деплой на Railway

1. Зарегистрируйся / войди на [railway.app](https://railway.app)
2. New Project → Deploy from GitHub (или Upload)
3. Лучший способ:
   - Создай репозиторий на GitHub и залей туда эту папку
   - Подключи репозиторий к Railway
4. Railway сам определит Python-приложение по `Procfile` и `requirements.txt`
5. В Variables (если нужно) ничего обязательного нет — база создаётся автоматически
6. После деплоя получишь публичный URL

### Альтернатива (без GitHub)
- В Railway: New → Empty Project → Deploy
- Или используй Railway CLI:
  ```bash
  npm i -g @railway/cli
  railway login
  railway init
  railway up
  ```

## Локальный запуск

```bash
cd charges-tracker
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Открой http://localhost:5000

## Структура
- `app.py` — бэкенд Flask + SQLite
- `templates/index.html` — интерфейс
- `requirements.txt` — зависимости
- `Procfile` — команда запуска для Railway
