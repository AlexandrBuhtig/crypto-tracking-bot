import requests
from telegram import Bot
import time
import os

# Токен Telegram бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Прямо указываем chat_id вашего канала
TELEGRAM_CHAT_ID = "@alexbinancebotcrypto"

# Список монет и их целевых цен
coins = {
    "fetch-ai": {"symbol": "FET", "target_buy": 1.00, "stop_loss": 0.70},
    "chainlink": {"symbol": "LINK", "target_buy": 20.00, "stop_loss": 15.00},
    "secret": {"symbol": "SCRT", "target_buy": 0.30, "stop_loss": 0.21},
    "avalanche-2": {"symbol": "AVAX", "target_buy": 30.00, "stop_loss": 22.00}
}

# Получение цены
def get_coin_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[coin_id]["usd"]

# Отправка сообщения
def send_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Стартовое сообщение
def send_startup_message():
    message = "🔍 Бот запущен. Отслеживаемые монеты:\n"
    for coin_id, info in coins.items():
        try:
            price = get_coin_price(coin_id)
            message += (
                f"• {info['symbol']}: текущая цена {price:.4f}$, "
                f"цель {info['target_buy']}$, стоп {info['stop_loss']}$\n"
            )
        except Exception as e:
            message += f"• {info['symbol']}: ошибка получения цены: {e}\n"
    send_message(message)

# Проверка цен
def track_prices():
    send_startup_message()
    while True:
        for coin_id, info in coins.items():
            try:
                price = get_coin_price(coin_id)
                symbol = info["symbol"]
                if price >= info["target_buy"]:
                    send_message(f"📈 {symbol} достиг цели! Цена: {price}$ — фиксируй прибыль!")
                elif price <= info["stop_loss"]:
                    send_message(f"⚠️ {symbol} достиг стоп-лосса! Цена: {price}$ — продавай!")
            except Exception as e:
                send_message(f"❗ Ошибка при проверке {info['symbol']}: {e}")
        time.sleep(300)  # 5 минут

if __name__ == "__main__":
    track_prices()
