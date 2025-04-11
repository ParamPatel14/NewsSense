import json
import os

def load_json_file(file_path):
    """Load a JSON file and return its contents."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")
        return []

def remove_null_values(obj):
    """Recursively remove null values from a dictionary."""
    if not isinstance(obj, dict):
        return obj
    return {
        k: remove_null_values(v)
        for k, v in obj.items()
        if v is not None
        for k, v in [(k, v) for k, v in obj.items() if v is not None]
        if isinstance(v, (dict, list)) and v or not isinstance(v, (dict, list))
    }

def search_ticker(ticker_input, json_files):
    """Search for a ticker or company name across JSON files."""
    for file_path in json_files:
        data = load_json_file(file_path)
        if not data:
            continue
        for obj in data:
            # Match ticker if not null, else match name
            if obj.get('ticker') and obj['ticker'].lower() == ticker_input.lower():
                return obj
            elif not obj.get('ticker') and obj.get('name') and obj['name'].lower() == ticker_input.lower():
                return obj
    return None

def save_to_json(obj, output_file):
    """Save the object to a JSON file."""
    try:
        with open(output_file, 'w') as f:
            json.dump(obj, f, indent=4)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")

def main():
    # List of JSON files to search
    json_files = [
    r'C:\Hackathon\NewsSense\Backend\Mf_holdings_data.json',
    r'C:\Hackathon\NewsSense\Backend\Mutual_funds_data.json',
    r'C:\Hackathon\NewsSense\Backend\Stock_data.json'
    ]
    
    # Get ticker input from user
    ticker_input = input("Enter the ticker or company name: ").strip()
    
    # Search for the ticker or name
    result = search_ticker(ticker_input, json_files)
    
    if result:
        # Remove null values
        cleaned_result = remove_null_values(result)
        
        # Save to a new JSON file
        output_file = 'output.json'
        save_to_json(cleaned_result, output_file)
    else:
        print(f"No match found for ticker or name: {ticker_input}")

if __name__ == "__main__":
    main()