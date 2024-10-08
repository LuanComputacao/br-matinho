import csv

from bs4 import BeautifulSoup

from scrapper.dentista import get_product_details, get_product_details_soup

BASE_URL = 'https://www.dentistaseeds.com/produtos'

def test_get_product_details__description_exists():
    # product_slug = 'm8-automatica'
    # product_url = f'{BASE_URL}/{product_slug}/'
    # soup = get_product_details_soup(product_url)
    text = """<div class="product-description user-content">
<p><strong>Linhagem</strong>: M8 x Auto</p>
<p><strong>THC:</strong> Geralmente varia entre 18% e 22%</p>
<p><strong>Tipo (%Sativa e %Indica):</strong> Híbrida, 60% Indica - 40% Sativa</p>
<p><strong>Floração:</strong> Em média, leva cerca de 8 a 10 semanas para florescer completamente</p>
<p><strong>Sabor:</strong> O sabor pode variar, mas geralmente apresenta notas terrosas e doces, com um toque de especiarias e frutas.</p>
<p><strong>Efeito: </strong>Oferece um efeito equilibrado que pode proporcionar uma sensação de euforia e relaxamento, com um leve aumento da criatividade e alívio do estresse. A variedade M8 é ideal para quem busca uma experiência de sabor e efeito versátil.</p>
</div>"""

    soup = BeautifulSoup(text, 'html.parser')

    details = get_product_details(soup)
    
    
    assert details is not None