import requests
import time
import os
from telegram import Bot

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

# Основной цикл для отслеживания цен
def track_prices():
    # Сообщение о запуске бота и отслеживаемых монетах
    send_message("Бот запущен и отслеживает следующие монеты с целевыми ценами:\n"
                 "FET: Target Buy = $1.00, Stop Loss = $0.70\n"
                 "LINK: Target Buy = $20.00, Stop Loss = $15.00\n"
                 "SCRT: Target Buy = $0.30, Stop Loss = $0.21\n"
                 "AVAX: Target Buy = $30.00, Stop Loss = $22.00\n")

    # Основной цикл для отслеживания цен
    while True:
        for coin, targets in coins.items():
            price = get_coin_price(coin)
            if price is None:
                continue  # Если не удалось получить цену, продолжаем следующий цикл

            # Отправка уведомлений, если цена достигла цели
            if price >= targets["target_buy"]:
                send_message(f"Цель по {coin} достигнута! Цена: {price} USD. Фиксируй прибыль!")
            elif price <= targets["stop_loss"]:
                send_message(f"Стоп-лосс по {coin} сработал! Цена: {price} USD. Продавай позицию!")

        # Проверка цен каждые 5 минут
        time.sleep(300)

# Запуск бота
if __name__ == "__main__":
    track_prices()
