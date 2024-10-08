import pytest
from scrapper.dentista import PRODUCT_DESCRIPTION_TOPICS, get_product_details_soup

BASE_URL = 'https://www.dentistaseeds.com/produtos'


def test_get_product_details_soup__retrieve_existent_description():
    product_slug = 'moby-dick-automatica'
    product_url = f'{BASE_URL}/tests/data/{product_slug}/'
    soup = get_product_details_soup(product_url)

    with open(f'{product_slug}.html', 'w') as file:
        file.write(soup.text)
    text = soup.text.strip()

    for info in PRODUCT_DESCRIPTION_TOPICS:
        if info not in text:
            assert False, f"Missing necessary info: {info}"


def test_get_product_details_soup__missing_sobre_a_genetica():
    product_slug = 'm8-automatica'
    product_url = f'{BASE_URL}/tests/data/{product_slug}/'
    soup = get_product_details_soup(product_url)

    with open(f'{product_slug}.html', 'w') as file:
        file.write(soup.text)
    text = soup.text.strip()

    for info in list(set(PRODUCT_DESCRIPTION_TOPICS) - set(['Sobre a Genética'])):
        if info not in text:
            assert False, f"Missing necessary info: {info}"
