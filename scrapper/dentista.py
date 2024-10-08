import csv
import json
import sqlite3
from typing import Union

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import Any

PAGE = 1
LIMIT = 200

REQUESTS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

CSV_HEADER = ['Product Name', 'Product URL', 'Linhagem', 'Sobre a Genética', 'THC', 'THC/CBD', 'CBD',
              'Tipo (%Sativa e %Indica)', 'Floração', 'Sabor', 'Efeito']
PRODUCT_DESCRIPTION_TOPICS = CSV_HEADER[2:]


def get_product_details(soup: Any) -> dict:
    description = {}
    for paragraph in soup.find_all('p'):
        print(f'Paragraph: ->{paragraph.text}<-')
        if not paragraph.text or ':' not in paragraph.text:
            continue

        tuple_description = (s.strip() for s in paragraph.text.split(':'))
        key, value = tuple_description
        if key in PRODUCT_DESCRIPTION_TOPICS:
            description[key] = value
        else:
            alternative_keys = {
                "Tipo": "Tipo (%Sativa e %Indica)"
            }
            description[alternative_keys[key]] = value

    return description


def get_product_details_soup(product_url) -> Union[Tag, NavigableString, None]:
    with open('urls.html', 'w') as file:
        file.write(product_url)
    response = requests.get(product_url, headers=REQUESTS_HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    return soup.find('div', class_='product-description')


# Function to scrape the website and write to CSV
def scrape_and_save_to_csv(url, output_file):
    try:
        # Send GET request with headers
        response = requests.get(url, headers=REQUESTS_HEADERS)
        response.raise_for_status()

        # Parse the response HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product information
        products = soup.find_all('div', class_='js-item-product')

        # Prepare CSV file to write
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADER)
            writer.writeheader()

            # Loop through each product and extract data
            for product in products:
                product_name = product.find('div', class_='js-item-name').text.strip()

                # Extract data-variants and parse it as JSON
                product_url = product.find('a', class_='item-link').get('href')
                print(f"Scraping product: {product_name}")
                print(f"Product URL: {product_url}")
                soup = get_product_details_soup(product_url)
                product_details = get_product_details(soup)

                writer.writerow({
                    'Product Name': product_name,
                    'Product URL': product_url,
                    **product_details
                })

        print("Data successfully written to", output_file)

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")


def load_csv_to_sqlite(csv_file, db_file):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_name TEXT,
            product_url TEXT,
            linhagem TEXT,
            sobre_a_genetica TEXT,
            thc TEXT,
            thc_cbd TEXT,
            cbd TEXT,
            tipo TEXT,
            floracao TEXT,
            sabor TEXT,
            efeito TEXT
        )
    ''')

    # Read CSV file and insert data into the table
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT INTO products (
                    product_name, product_url, linhagem, sobre_a_genetica, thc, thc_cbd, cbd, tipo, floracao, sabor, efeito
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Product Name'], row['Product URL'], row['Linhagem'], row['Sobre a Genética'], row['THC'],
                row['THC/CBD'], row['CBD'], row['Tipo (%Sativa e %Indica)'], row['Floração'], row['Sabor'],
                row['Efeito']
            ))

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Main function to trigger the scraper
if __name__ == "__main__":
    url = f"https://www.dentistaseeds.com/produtos/page/{PAGE}/?results_only=true&limit={LIMIT}&theme=amazonas"
    output_file = 'products.csv'

    print("Starting the scraping process...")
    scrape_and_save_to_csv(url, output_file)
    print("Scraping completed.")

    print("Starting the SQLite database process...")
    load_csv_to_sqlite(output_file, 'products.db')
    print("Database process completed.")
