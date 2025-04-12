import matplotlib
matplotlib.use('Agg')
import spacy
import requests
import yfinance as yf
import json
import matplotlib.pyplot as plt
from PIL import Image
import io
# Load spaCy model
nlp = spacy.load("en_core_web_sm")
import os


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



    
def plot_5_day_trend(ticker, name, url="./stock_images"):
    """
    Fetches 5-day stock data for a given ticker, plots the closing price trend,
    opens and saves the plot as a PNG image using Pillow, and returns the file path.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        name (str): The name of the stock/company for the plot title and filename.
        url (str): The directory path to save the image file. Defaults to './stock_images'.

    Returns:
        str or None: The full file path of the saved image, or None if an error occurred
                     or no data was available.
    """
    file_path = None  # Initialize file_path to None, returned on failure
    try:
        # Ensure the target directory exists, create if it doesn't
        os.makedirs(url, exist_ok=True)
        # Define the full path for the image file
        file_path = os.path.join(url, f"{name}.png")

        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)
        # Fetch 5 days of daily data
        hist = stock.history(period='5d', interval='1d')

        # Check if data was retrieved
        if hist.empty:
            print(f"No data available for 5-day trend for {ticker}.")
            return None # Return None explicitly if no data

        # Create the plot using matplotlib
        plt.figure(figsize=(10, 5))
        # Format date for better readability on the x-axis
        plt.plot(hist.index.strftime('%Y-%m-%d'), hist['Close'], marker='o', linestyle='-', color='blue', label='Close Price')
        plt.title(f"5-Day Stock Price Trend for {name} ({ticker})")
        plt.xlabel("Date")
        plt.ylabel("Close Price (USD)")
        plt.grid(True)
        plt.xticks(rotation=45) # Rotate date labels for better fit
        plt.legend()
        plt.tight_layout() # Adjust plot for tight layout

        # Save the plot to an in-memory buffer (BytesIO)
        buf = io.BytesIO()
        plt.savefig(buf, format='PNG')
        plt.close() # Close the plot figure to free up memory
        buf.seek(0) # Rewind the buffer to the beginning

        # Open the image from the buffer using Pillow's Image.open()
        img = Image.open(buf)

        # Check if the image object was created successfully
        if img:
            # Save the image object to the specified file path using Pillow's save()
            img.save(file_path, "PNG")
            print(f"Image saved successfully to: {file_path}")
        else:
            # This case is unlikely if savefig to buffer succeeded, but good practice
            print("Error: Could not create image object from buffer.")
            file_path = None # Ensure None is returned if image creation failed

        buf.close() # Close the BytesIO buffer

    except Exception as e:
        print(f"Error processing stock data for {ticker}: {e}")
        # Attempt to close any lingering plot figure in case of error mid-plot
        if plt.gcf().get_axes():
             plt.close()
        file_path = None # Ensure None is returned on any exception

    # Return the file path (will be None if any step failed)
    return file_path


# Main Flow 
def main_flow_extract_name():
    query = input("Enter your query: ")
    company = extract_company_name(query)

    name=None
    ticker=None
    if company:
        print("Extracted stock:", company)
        name, ticker = get_ticker_yahoo(company)
        if ticker:
            print(f"Found ticker: {ticker} ({name})")
            show_yesterdays_stock_change(ticker, name)
            image=plot_5_day_trend(ticker, name)
            return image,name,ticker
        
        else:
            print("No ticker found.")
    else:
        print("Could not extract a stock name.")