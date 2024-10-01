import csv
import json
from typing import Union

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


from typing import Any


def get_product_details(soup: Any):
# Check if the description exists
    if soup:
        paragraphs = soup.find_all('p')
        # Extract the text from each paragraph and join them into one string
        description_text = [p.text.strip().split(': ') for p in paragraphs]
        for i in range(len(description_text)):
            description_text[i] = description_text[i][1] if len(description_text[i]) > 1 else description_text[i][0]
    else:
        description_text = None

    return description_text


def get_product_details_soup(product_url) -> (Tag | NavigableString | None):
    response = requests.get(product_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    return soup.find('div', class_='product-description')


# Function to scrape the website and write to CSV
def scrape_and_save_to_csv(url, output_file):
    
    try:
        # Send GET request with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the response HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product information
        products = soup.find_all('div', class_='js-item-product')

        # Prepare CSV file to write
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Price', 'Quantity', 'Image URL', 'Product URL', 'Genética', 'THC', 'CBD', 'Tipo', 'Floração', 'Sabor', 'Efeito'])

            # Loop through each product and extract data
            for product in products:
                product_name = product.find('div', class_='js-item-name').text.strip()
                price = product.find('span', class_='js-price-display').text.strip()
                quantity = product.find('select', class_='js-variation-option').find('option', selected=True).text.strip()
                image_url = product.find('img', class_='js-item-image')['data-srcset'].split(',')[0].strip().split(' ')[0]
                image_url = "https:" + image_url  # Fix image URL

                # Extract data-variants and parse it as JSON
                product_url = product.find('a', class_='item-link').get('href')
                
                product_details = get_product_details(product_url)
                # Write to CSV (variants as JSON string)
                writer.writerow([product_name, price, quantity, image_url, product_url, *product_details])

        print("Data successfully written to", output_file)
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

# Main function to trigger the scraper
if __name__ == "__main__":
    url = "https://www.dentistaseeds.com/automaticas/page/1/?results_only=true&limit=200&theme=amazonas"
    output_file = 'products.csv'
    
    print("Starting the scraping process...")
    scrape_and_save_to_csv(url, output_file)
    print("Scraping completed.")



