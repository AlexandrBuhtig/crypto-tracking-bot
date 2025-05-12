# Crypto Price Tracker Telegram Bot

Этот бот отслеживает цены указанных криптовалют с использованием API CoinGecko и присылает уведомления в Telegram, если цена достигает целевых уровней (фиксация прибыли или стоп-лосс).

## 🧠 Возможности

- Получение актуальных цен с CoinGecko.
- Уведомления о достижении целевой цены или стоп-лосса.
- Поддержка нескольких криптомонет.
- Автоматический запуск каждые 5 минут.

## 🚀 Запуск на Render

1. **Создай репозиторий на GitHub** и загрузи туда:
   - `bot.py`
   - `requirements.txt`
   - `.gitignore`
   - `README.md`

2. **Создай веб-сервис в [Render](https://render.com/)**:
   - Тип: **Web Service**
   - Environment: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

3. **Добавь переменные окружения в Render**:
   - `TELEGRAM_BOT_TOKEN`: токен от BotFather
   - `TELEGRAM_CHAT_ID`: ID чата или канала (например, `-1001234567890`)

## 🛠 Зависимости

Установлены в `requirements.txt`:

```txt
requests
python-telegram-bot==13.15
