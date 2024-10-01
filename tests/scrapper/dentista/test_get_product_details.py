import csv

from scrapper.dentista import get_product_details


def test_get_product_details__description_exists():
    product_url = 'https://www.dentistaseeds.com/produtos/moby-dick-automatica/'
    # store the result into a csv
    result = get_product_details(product_url)
    with open('result.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(result)
    expected = ['Sativa', 'High', 'Low', 'Feminizada', '8-9 semanas', 'Cítrico', 'Energético']
    assert get_product_details(product_url) == expected