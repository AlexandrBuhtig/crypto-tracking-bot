import requests
import time
import os
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Токен Telegram бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CMC_API_KEY = os.getenv("CMC_API_KEY")  # Получаем ключ CoinMarketCap из переменных окружения
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Список монет и их целевых цен
coins = {
    "FET": {"target_buy": 1.00, "stop_loss": 0.70},
    "LINK": {"target_buy": 20.00, "stop_loss": 15.00},
    "SCRT": {"target_buy": 0.30, "stop_loss": 0.21},
    "AVAX": {"target_buy": 30.00, "stop_loss": 22.00}
}

# Инициализация Flask приложения
app = Flask(__name__)

# Функция для получения текущей цены монеты через CoinMarketCap
def get_coin_price(symbol):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {
        "symbol": symbol,
        "convert": "USD"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY  # Используем API ключ
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["data"][symbol]["quote"]["USD"]["price"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных для {symbol}: {e}")
        return None

# Функция для отправки сообщения в Telegram
def send_message(message):
    chat_id = '@alexbinancebotcrypto'  # Канал, куда будут отправляться сообщения
    bot.send_message(chat_id=chat_id, text=message)

# Функция для отслеживания цен
def track_prices():
    for coin, targets in coins.items():
        price = get_coin_price(coin)
        if price is None:
            continue  # Если не удалось получить цену, продолжаем следующий цикл

        # Отправка уведомлений, если цена достигла цели
        if price >= targets["target_buy"]:
            send_message(f"Цель по {coin} достигнута! Цена: {price} USD. Фиксируй прибыль!")
        elif price <= targets["stop_loss"]:
            send_message(f"Стоп-лосс по {coin} сработал! Цена: {price} USD. Продавай позицию!")

# Функция для отправки ежедневных уведомлений в 5 UTC
def daily_update():
    message = "Текущие цены на монеты и целевые цены:\n"
    for coin, targets in coins.items():
        price = get_coin_price(coin)
        if price is None:
            message += f"{coin}: Не удалось получить цену\n"
        else:
            message += (f"{coin}: {price} USD\n"
                        f"Target Buy: {targets['target_buy']} USD, "
                        f"Stop Loss: {targets['stop_loss']} USD\n")
    
    send_message(message)

# Инициализация планировщика задач APScheduler
scheduler = BackgroundScheduler()

# Запускаем функцию отслеживания цен раз в 3 часа
scheduler.add_job(
    track_prices, 
    IntervalTrigger(hours=3),  # Интервал: раз в 3 часа
    id='track_prices',
    name='Track coin prices every 3 hours',
    replace_existing=True
)

# Запускаем функцию ежедневного обновления в 5:00 UTC
scheduler.add_job(
    daily_update, 
    'cron',  # Используем cron для задания по времени
    hour=5,  # 5:00 UTC
    minute=0,
    second=0,
    id='daily_update',
    name='Send daily update at 5 UTC',
    replace_existing=True
)

# Запуск планировщика задач
scheduler.start()

# Маршрут для Flask
@app.route('/')
def index():
    prices_message = "Текущие цены на монеты:\n"
    for coin in coins:
        price = get_coin_price(coin)
        if price:
            prices_message += f"{coin}: {price} USD\n"
        else:
            prices_message += f"{coin}: Не удалось получить цену\n"
    return prices_message

# Запуск приложения Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
