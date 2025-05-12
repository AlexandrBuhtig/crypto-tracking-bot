import requests
from telegram import Bot
import time
import os

# Токен Telegram бота (используется переменная окружения или напрямую)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Список монет и их целевых цен
coins = {
    "FET": {"target_buy": 1.00, "stop_loss": 0.70},
    "LINK": {"target_buy": 20.00, "stop_loss": 15.00},
    "SCRT": {"target_buy": 0.30, "stop_loss": 0.21},
    "AVAX": {"target_buy": 30.00, "stop_loss": 22.00}
}

# Функция для получения текущей цены монеты
def get_coin_price(coin):
    coin_ids = {
        "FET": "fetch-ai",
        "LINK": "chainlink",
        "SCRT": "secret",
        "AVAX": "avalanche-2"
    }
    coin_id = coin_ids.get(coin.upper())
    if not coin_id:
        return None
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    print(f"DEBUG: Coin {coin} → {coin_id}, Response: {data}")  # Добавлено для отладки
    return data.get(coin_id, {}).get("usd")

# Функция для отправки сообщения в Telegram
def send_message(message):
    bot.send_message(chat_id='@alexbinancebotcrypto', text=message)

# Основной цикл, проверяющий цены
def track_prices():
    while True:
        for coin, targets in coins.items():
            price = get_coin_price(coin)
            if price is None:
                continue
            if price >= targets["target_buy"]:
                send_message(f"🚀 Цель по {coin} достигнута! Цена: {price:.2f} USD. Фиксируй прибыль!")
            elif price <= targets["stop_loss"]:
                send_message(f"⚠️ Стоп-лосс по {coin}! Цена: {price:.2f} USD. Продавай позицию!")
        time.sleep(300)  # Проверка каждые 5 минут

if __name__ == "__main__":
    track_prices()
