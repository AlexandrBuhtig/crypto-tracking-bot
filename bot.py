import requests
from telegram import Bot
import time
import os
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен Telegram бота из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Установи это значение в Render
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Список монет и их целевых значений
coins = {
    "fet": {"target_buy": 1.00, "stop_loss": 0.70},
    "link": {"target_buy": 20.00, "stop_loss": 15.00},
    "scrt": {"target_buy": 0.30, "stop_loss": 0.21},
    "avax": {"target_buy": 30.00, "stop_loss": 22.00}
}

# Получение текущей цены монеты
def get_coin_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if coin_id in data:
            return data[coin_id]["usd"]
        else:
            logging.warning(f"[!] Coin '{coin_id}' not found in API response.")
            return None
    except Exception as e:
        logging.error(f"[Ошибка] Не удалось получить цену для {coin_id}: {e}")
        return None

# Отправка уведомлений
def send_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info(f"[INFO] Отправлено сообщение: {message}")
    except Exception as e:
        logging.error(f"[Ошибка отправки в Telegram] {e}")

# Основной цикл
def track_prices():
    while True:
        for coin_id, levels in coins.items():
            price = get_coin_price(coin_id)
            if price is None:
                continue
            if price >= levels["target_buy"]:
                send_message(f"📈 {coin_id.upper()} достиг цели — ${price:.2f}. Рекомендуется фиксировать прибыль.")
            elif price <= levels["stop_loss"]:
                send_message(f"📉 {coin_id.upper()} ниже стоп-лосса — ${price:.2f}. Рекомендуется продать позицию.")
            else:
                logging.info(f"{coin_id.upper()}: ${price:.2f} — в пределах нормы.")
        time.sleep(300)  # Проверка каждые 5 минут

if __name__ == "__main__":
    send_message("🤖 Бот отслеживания криптовалют запущен.")
    track_prices()
