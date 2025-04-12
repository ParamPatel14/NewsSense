import spacy
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import io

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_company_name(query):
    """
    Extracts company name from the user input using spaCy.
    """
    doc = nlp(query)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            return ent.text.strip()
    tokens = [token.text for token in doc if token.text[0].isupper() and token.is_alpha and not token.is_stop]
    return " ".join(tokens[:3]) if tokens else None


def get_ticker_yahoo(company_name):
    """
    Fetches ticker symbol from Yahoo Finance using the company name.
    """
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


def show_stock_change_5_days(ticker, name):
    """
    Displays the percentage change in stock price over the last 5 days.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='5d', interval='1d')  # Get last 5 days

        if hist.empty or len(hist) < 5:
            return None

        # Get the closing price on the first and last day
        first_day_close = hist.iloc[0]['Close']
        last_day_close = hist.iloc[-1]['Close']

        # Calculate the percentage change
        percent_change = ((last_day_close - first_day_close) / first_day_close) * 100
        percent_change = round(percent_change, 2)

        return percent_change

    except Exception as e:
        return None



def plot_stock_trend_multiple_periods(ticker, name, save_images=False):
    """
    Plots stock price trends for different time periods (5 days, 1 month, 3 months, 6 months, 1 year).
    Optionally saves the images as JPEG files using Pillow.
    """
    try:
        stock = yf.Ticker(ticker)
        periods = {
            "5 Days": "5d",
            "1 Month": "1mo",
            "3 Months": "3mo",
            "6 Months": "6mo",
            "1 Year": "1y"
        }

        image_paths = []

        for label, period in periods.items():
            hist = stock.history(period=period, interval='1d')

            if hist.empty:
                continue

            # Plotting each period's data
            plt.figure(figsize=(10, 5))
            plt.plot(hist.index, hist['Close'], marker='o', linestyle='-', color='blue', label='Close Price')
            plt.title(f"{label} Stock Price Trend for {name} ({ticker})")
            plt.xlabel("Date")
            plt.ylabel("Close Price (USD)")
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()

            # Save the plot as a .jpeg image using Pillow
            if save_images:
                image_path = f"{name}_{ticker}_{label.replace(' ', '_')}.jpeg"
                plt.savefig(image_path, format="jpeg")
                image_paths.append(image_path)

            plt.close()  # Close the plot to free memory

        return image_paths

    except Exception as e:
        return None


# -------- Streamlit App --------
st.title("Stock Analysis App")

# User input
query = st.text_input("Enter a company name or stock-related query:")

if query:
    company = extract_company_name(query)

    if company:
        st.write(f"Extracted company: {company}")

        name, ticker = get_ticker_yahoo(company)

        if ticker:
            st.write(f"Found ticker: {ticker} ({name})")

            # Show percentage change
            percent_change = show_stock_change_5_days(ticker, name)
            if percent_change is not None:
                st.write(f"The stock has {'increased' if percent_change > 0 else 'dipped'} by {abs(percent_change)}%")
            else:
                st.write("No recent stock data available.")

            # Show stock price trend visualizations
            images = plot_stock_trend_multiple_periods(ticker, name, save_images=True)

            if images:
                for image in images:
                    img = Image.open(image)
                    st.image(img, caption=f"Stock Trend for {name} ({ticker})")
            else:
                st.write("No visualizations available.")
        else:
            st.write("No ticker found.")
    else:
        st.write("Could not extract a stock name.")
