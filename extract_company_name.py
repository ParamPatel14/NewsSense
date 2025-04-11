import spacy
import requests
import yfinance as yf
import json
import matplotlib.pyplot as plt

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_company_name(query):
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            return ent.text.strip()
    tokens = [token.text for token in doc if token.text[0].isupper() and token.is_alpha and not token.is_stop]
    return " ".join(tokens[:3]) if tokens else None


def get_ticker_yahoo(company_name):
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={company_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        results = data.get("quotes", [])
        if results:
            first_result = results[0]
            return first_result.get("shortname"), first_result.get("symbol")
    return None, None


def show_yesterdays_stock_change(ticker, name):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='2d', interval='1d')  # Get last 2 days

        if hist.empty or len(hist) < 1:
            print(f"No recent stock data found for {name} ({ticker})")
            return

        latest = hist.iloc[-1]  # Yesterday's/latest row

        open_price = latest['Open']
        close_price = latest['Close']
        percent_change = ((close_price - open_price) / open_price) * 100
        percent_change = round(percent_change, 2)

        direction = "increased" if percent_change > 0 else "dipped" if percent_change < 0 else "remained unchanged"

        # Output
        print(f"\nThe stock has {direction} by {abs(percent_change)}%")

    except Exception as e:
        print("Error fetching yesterday's stock data:", e)


def plot_5_day_trend(ticker, name):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='5d', interval='1d')

        if hist.empty:
            print("No data available for 5-day trend.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], marker='o', linestyle='-', color='blue', label='Close Price')
        plt.title(f"5-Day Stock Price Trend for {name} ({ticker})")
        plt.xlabel("Date")
        plt.ylabel("Close Price (USD)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("Error plotting stock data:", e)


# Main Flow 
query = input("Enter your query: ")
company = extract_company_name(query)

if company:
    print("Extracted stock:", company)
    name, ticker = get_ticker_yahoo(company)
    if ticker:
        print(f"Found ticker: {ticker} ({name})")
        show_yesterdays_stock_change(ticker, name)
        plot_5_day_trend(ticker, name)
    else:
        print("No ticker found.")
else:
    print("Could not extract a stock name.")

