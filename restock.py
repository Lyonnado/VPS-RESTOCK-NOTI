import time
import cloudscraper
from bs4 import BeautifulSoup
import requests

# Telegram 设置
TELEGRAM_TOKEN = '你的tg_bot token'
USER_ID = 你的userid

# 要监控的 URL 列表
URLS = [
    "https://legendvps.com/store/singapore/sg-evo-1-1g-sip",
    "https://***",
    # 添加更多链接
]

scraper = cloudscraper.create_scraper()
out_of_stock_keywords = ["Out of Stock", "售罄", "缺货"]

while True:
    for url in URLS:
        response = scraper.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()

        if any(keyword.lower() in page_text.lower() for keyword in out_of_stock_keywords):
            print(f"❌ 无货：{url}")
        else:
            print(f"✅ 有货：{url}")
            # 每次有货都发送 Telegram 通知
            msg = f"🚨 有货啦！\n{url}"
            tg_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.get(tg_api, params={"chat_id": USER_ID, "text": msg})

    time.sleep(10)
