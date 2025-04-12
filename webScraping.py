import requests
from bs4 import BeautifulSoup
import re





    




def get_info_from_website(url,search_word,text_content,tags_to_search):
    try:

        response = requests.get(url)
        response.raise_for_status() 

   
        soup = BeautifulSoup(response.text, 'html.parser')

        # print(f"Searching for the word '{search_word}' in tags {tags_to_search} on {url}\n")
        found_elements = 0

        
        elements = soup.find_all(tags_to_search)

        
        for element in elements:
            if element=='a':
                element_text=element.get("innerHTML")
            element_text = element.get_text()
            
            if re.search(r'\b' + re.escape(search_word) + r'\b', element_text, re.IGNORECASE):

                text_content+=element_text+"\n"
                
                # with open(r"C:\Users\spune\Desktop\{}_data.txt".format(search_word),"a") as file:

                #     # print(f"Found '{search_word}' in tag <{element.name}>:")
                #     # print("-" * 20) # Separator
                #     file.write(element_text.strip())
                #     file.write('\n')
                #     file.write('\n')
                    # print("-" * 20 + "\n") # Separator
                    # found_elements += 1
# 
        # if found_elements == 0:
        #     print(f"The word '{search_word}' was not found in any of the specified tags.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")




def get_text_content(search_word):
    list_url = ['https://www.indiatoday.in/business/market']
    for i in range(1,6):
        list_url.append(f'https://www.moneycontrol.com/news/business/page-{i}')
    for i in range(1,6):
        list_url.append(f"https://www.moneycontrol.com/news/business/markets/page-{i}")
    for i in range(1,6):
        list_url.append(f"https://www.moneycontrol.com/news/business/stocks/page-{i}")

    for i in range (1,6):
        list_url.append(f"https://www.moneycontrol.com/news/business/companies/page-{i}")

    for i in range(1,6):
        list_url.append(f"https://www.moneycontrol.com/news/trends/page-{i}")
    text_content=""
    tags_to_search = ['a','p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    for url in list_url:
        get_info_from_website(url,search_word,text_content,list_url)
    return text_content


# import requests
# from bs4 import BeautifulSoup
# import re
# import json 


# list_url = ['https://www.indiatoday.in/business/market']


# base_urls = [
#     'https://www.moneycontrol.com/news/business/page-{}',
#     'https://www.moneycontrol.com/news/business/markets/page-{}',
#     'https://www.moneycontrol.com/news/business/stocks/page-{}',
#     'https://www.moneycontrol.com/news/business/companies/page-{}',
#     'https://www.moneycontrol.com/news/trends/page-{}'
# ]


# for base in base_urls:
#     for i in range(1, 6): # Pages 1 to 5
#         list_url.append(base.format(i))

# search_word = 'IBM'
# # Tags where the search_word will be looked for
# tags_to_search = ['a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
# # File where the final dictionary will be saved
# output_json_file = r"C:\Users\spune\Desktop\NewsSense\extracted_{}_data.json".format(search_word)


# extracted_content_in_json = {}


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }


# def get_info_from_website(url, search_word, results_dict):
   
#     try:
#         print(f"Requesting: {url}")
#         # Make the HTTP GET request with headers and a timeout
#         response = requests.get(url, headers=headers, timeout=20)
#         # Check if the request was successful 
#         response.raise_for_status()

#         print(f"Parsing: {url}")
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find all HTML elements matching the tags 
#         elements = soup.find_all(tags_to_search)
#         # List to hold text snippets found *on this specific page*
#         found_snippets_for_url = []

#         # Iterate through each found element
#         for element in elements:
#             # Extract the text content, removing leading/trailing whitespace
#             element_text = element.get_text(strip=True)

#             # Check if the extracted text is not empty and contains the search_word
#             # Uses regex for a case-insensitive, whole-word search
#             if element_text and re.search(r'\b' + re.escape(search_word) + r'\b', element_text, re.IGNORECASE):
#                 # If found, add the cleaned text snippet to our list for this URL
#                 found_snippets_for_url.append(element_text)

#         # After checking all elements on the page, if we found any relevant snippets...
#         if found_snippets_for_url:
#             # Add/Update the entry in the main dictionary
#             # The key is the url, the value is the list of snippets found
#             results_dict[url] = found_snippets_for_url
#             print(f"Found {len(found_snippets_for_url)} snippet(s) containing '{search_word}' on {url}")
        

#     # Handle potential errors during the request/parsing
#     except requests.exceptions.Timeout:
#         print(f"Timeout error when fetching URL {url}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request error for URL {url}: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred while processing {url}: {e}")


# # --- Main Execution Logic ---
# print(f"Starting scraping process to find '{search_word}'...")
# print("-" * 40)

# # Loop through each URL in the list
# for url in list_url:
#     # Call the function to process the URL and update the dictionary
#     get_info_from_website(url, search_word, extracted_content_in_json)
#     print("-" * 40) # Print a separator line

# print("Scraping process completed.")
# print("-" * 40)



# # Save the dictionary to a JSON file
# print(f"Saving the extracted data to '{output_json_file}'...")
# try:
#     # Open the file in write mode ('w') with UTF-8 encoding
#     with open(output_json_file, 'w', encoding='utf-8') as f:
#         # Write the Python dictionary to the file as JSON
#         json.dump(extracted_content_in_json, f, indent=4, ensure_ascii=False)
#     print(f"Successfully saved data to '{output_json_file}'")
# except IOError as e:
#     print(f"Error: Could not write to file '{output_json_file}'. Reason: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred while saving JSON: {e}")