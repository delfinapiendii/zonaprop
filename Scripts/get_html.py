# get_html.py
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc

# Mantén el resto de tus importaciones

def get_info(compra_alquiler_list, barrio_list, max_ambientes, contador, driver): # Se elimina min_ambientes
    """
    Construye y navega a la URL de ZonaProp con filtros específicos.

    Args:
        compra_alquiler_list (list): Lista de cadenas para definir si es compra o alquiler (ej. ['alquiler']).
        barrio_list (list): Lista de cadenas con el/los barrio/s (ej. ['colegiales']).
        max_ambientes (int): Número máximo de ambientes.
        contador (int): Número de página.
        driver: Instancia de Undetected Chrome Driver.

    Returns:
        BeautifulSoup: Objeto BeautifulSoup de la página scrapeada.
    """
    # Definir si compra y/o alquiler (ahora solo se esperaría ['alquiler'] para 'alquiler')
    compra_alquiler_str = '-'.join(compra_alquiler_list) 

    # Definir barrio - ahora con el prefijo 'q-'
    barrio_str = '-'.join(barrio_list) if len(barrio_list) > 1 else barrio_list[0]
    barrio_url_part = f"q-{barrio_str}" # Añadimos el prefijo 'q-'

    # Construir la parte de los ambientes para la URL (ej. 'hasta-5-ambientes')
    ambientes_part = ""
    if max_ambientes is not None:
        ambientes_part = f"-hasta-{max_ambientes}-ambientes"

    # Construir la URL completa con la nueva estructura
    # Formato esperado: departamentos-{alquiler}{ambientes_part}-{q-barrio}.html
    if contador is None or contador == 1: # Para la primera página, omitimos "-pagina-1"
        url = f"https://www.zonaprop.com.ar/departamentos-{compra_alquiler_str}{ambientes_part}-{barrio_url_part}.html"
    else:
        url = f"https://www.zonaprop.com.ar/departamentos-{compra_alquiler_str}{ambientes_part}-{barrio_url_part}-pagina-{contador}.html"

    # ¡Esta línea es clave para depurar! Te mostrará la URL que el driver intenta visitar.
    print(f"URL generada por get_html.py: {url}") 
    
    time.sleep(3) # Pausa para evitar bloqueos
    driver.get(url) # El driver navega a la URL construida
    html = driver.page_source
    
    # Usar BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html, "html.parser")

    return soup