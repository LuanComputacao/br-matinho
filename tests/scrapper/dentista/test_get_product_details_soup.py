from scrapper.dentista import get_product_details_soup


def test_get_product_details_soup__retrieve_existent_description():
    product_url = 'https://www.dentistaseeds.com/produtos/moby-dick-automatica/'
    soup = get_product_details_soup(product_url)
    
    with open('moby-dick-automatica.html') as file:
        file.write(soup)
    text = soup.text.strip()
    necessary_info = ['Linhagem', 'THC', 'Tipo (%Sativa e %Indica)', 'Floração', 'Sabor', 'Efeito']
    
    # Check if the text has the necessary info
    for info in necessary_info:
        if info not in text:
            assert False, f"Missing necessary info: {info}"