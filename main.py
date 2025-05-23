import requests
import time
import datetime

# Telegram 配置
BOT_TOKEN = '7921143457:你的Token'  # 确保包含冒号
CHAT_ID = '7052572465'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
        if response.status_code != 200:
            print(f"发送失败：{response.text}")
    except Exception as e:
        print(f"Telegram发送异常：{e}")

def fetch_eth_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    response = requests.get(url).json()
    return float(response['price'])

def main_loop():
    last_price = 0
    while True:
        try:
            price = fetch_eth_price()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            if last_price == 0:
                last_price = price
                send_telegram_message(f"[{now}] ETH 当前价格：{price:.2f} USDT")
            elif abs(price - last_price) / last_price > 0.01:
                send_telegram_message(f"[{now}] ETH 价格变动超 1%：{last_price:.2f} → {price:.2f}")
                last_price = price
        except Exception as e:
            print(f"运行时错误：{e}")
        time.sleep(3600)

# 程序入口
if __name__ == "__main__":
    send_telegram_message("✅ Bot 启动成功，开始监测 ETH 价格...")
    main_loop()

