import requests
from datetime import date, timedelta
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
check_news = False

# ------------------------------- CHECK PRICE FLUCTUATION ------------------------------ #
today = date.today()
yesterday = str(today - timedelta(days=1))
day_before = str(today - timedelta(days=2))

alphavantage_apikey = ""
parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alphavantage_apikey
}
stock = requests.get("https://www.alphavantage.co/query", params=parameters_stock)
stock.raise_for_status()
stock_data = stock.json()["Time Series (Daily)"]

price_yesterday = 0
price_day_before = 0
fluctuation = ""

for key, value in stock_data.items():
    if key == yesterday:
        price_yesterday = float(value["4. close"])
    if key == day_before:
        price_day_before = float(value["4. close"])
price_change = abs((price_yesterday - price_day_before)*100/price_day_before)
if price_yesterday - price_day_before > 0:
    fluctuation = "🔺"
else:
    fluctuation = "🔻"
if price_change > 5:
    check_news = True
else:
    print(f"Fluctuation in {COMPANY_NAME} stock price is: {fluctuation}{price_change}%")

# ------------------------------- CHECK NEWS ------------------------------ #
newsapi_key = ""
parameters_news = {
    "q": COMPANY_NAME,
    "from": day_before,
    "to": today,
    "sortBy": "popularity",
    "apiKey": newsapi_key
}

news = requests.get("https://newsapi.org/v2/everything", params=parameters_news)
news.raise_for_status()
news_data = news.json()["articles"]

links_to_send = []
message = ""

for item in news_data[0:3]:
    links_to_send.append(item)
for item in links_to_send:
    message += f"{STOCK}: {fluctuation}{round(price_change, 2)}%\n" \
               f"Headline: {item['title']}\nBrief: {item['description']}\nLink: {item['url']}\n\n"

# ------------------------------- SEND NEWS ------------------------------ #
email = ""
pw = ""

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=email, password=pw)
    connection.sendmail(from_addr=email, to_addrs="huy.130297@gmail.com",
                        msg=f"Subject:{STOCK} price alert\n\n{message.encode('utf-8')}")
