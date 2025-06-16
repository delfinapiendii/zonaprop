"""
Run this script to scrape all pages of ZonaProp listings
for all CABA barrios, then export everything to Excel.
Determina automáticamente el número de páginas por barrio usando la paginación.
"""
import os
import time
import pandas as pd
import undetected_chromedriver as uc
from get_html import get_info
from get_property_information import (
    get_price, get_location,
    get_house_information, get_link, get_id
)

# Lista de barrios (slugs) de CABA
BARRIOS = [
    'agronomia', 'almagro', 'balvanera', 'barracas', 'belgrano', 'boca',
    'boedo', 'caballito', 'chacarita', 'coghlan', 'colegiales', 'constitucion',
    'flores', 'floresta', 'la-paternal', 'liniers', 'mataderos', 'monte-castro',
    'montserrat', 'nueva-pompeya', 'nunez', 'palermo', 'parque-avellaneda',
    'parque-chacabuco', 'parque-chas', 'parque-patricios', 'puerto-madero',
    'recoleta', 'retiro', 'saavedra', 'san-cristobal', 'san-nicolas', 'san-telmo',
    'versalles', 'villa-crespo', 'villa-devoto', 'villa-general-mitre',
    'villa-lugano', 'villa-luro', 'villa-ortuzar', 'villa-pueyrredon',
    'villa-real', 'villa-riachuelo', 'villa-santa-rita', 'villa-urquiza',
    'villa-del-parque', 'velez-sarsfield'
]

OUTPUT_FILE = os.path.join(os.getcwd(), 'zonaprop_data.xlsx')


def get_page_count(soup):
    """Determina la cantidad de páginas disponibles usando la paginación de la página"""
    div_paging = soup.find('div', class_='paging-module__container-paging')
    if not div_paging:
        return 1
    page_nums = []
    for a in div_paging.find_all('a'):
        try:
            num = int(a.get_text().strip())
            page_nums.append(num)
        except ValueError:
            continue
    return max(page_nums) if page_nums else 1


def run_scraper():
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    all_records = []

    try:
        for barrio in BARRIOS:
            # Página inicial
            url0 = f"https://www.zonaprop.com.ar/departamentos-alquiler-{barrio}.html"
            print(f"⏳ Cargando página inicial: {url0}")
            soup0 = get_info(['alquiler'], [barrio], None, 1, driver)

            pages = get_page_count(soup0)
            print(f"✅ Barrio '{barrio}': {pages} páginas detectadas.")

            for page in range(1, pages + 1):
                if page == 1:
                    soup = soup0
                else:
                    url = f"https://www.zonaprop.com.ar/departamentos-alquiler-{barrio}-pagina-{page}.html"
                    print(f"  → Scrapeando {url}")
                    soup = get_info(['alquiler'], [barrio], None, page, driver)
                    time.sleep(1)

                cards = soup.find_all(
                    'div', class_='postingsList-module__card-container'
                )
                count = 0
                for card in cards:
                    try:
                        price, currency = get_price(card)
                        address, neighborhood = get_location(card)
                        info = get_house_information(card)
                        url_post = get_link(card)
                        prop_id = get_id(card)
                        all_records.append({
                            'ID': prop_id,
                            'URL': url_post,
                            'Barrio': neighborhood,
                            'Direccion': address,
                            'Info': info,
                            'Moneda': currency,
                            'Precio': price,
                        })
                        count += 1
                    except Exception:
                        continue
                print(f"    Página {page}: {count} anuncios procesados.")

    finally:
        driver.quit()

    df = pd.DataFrame(all_records)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n🎉 Scraping completo: {len(df)} registros guardados en '{OUTPUT_FILE}'")


if __name__ == '__main__':
    run_scraper()
