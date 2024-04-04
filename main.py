from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def obtener_informacion_patente(patente):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3')  
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://tributariomuni.gob.ar/samweb/index.php?r=/objeto/objeto/index&to=11")

        select_objeto = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tobj")))

        for option in select_objeto.find_elements(By.TAG_NAME, "option"):
            if option.text == "Automotores":
                option.click()
                break

        input_patente = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "identificador")))

        input_patente.send_keys(patente)

        boton_entrar = driver.find_element(By.ID, "entrar")
        boton_entrar.click()

        datos_periodos_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "datosPeriodos")))

        pagina_source = driver.page_source

        soup = BeautifulSoup(pagina_source, "html.parser")

        info_div = soup.find("div", id="datosGenerales")

        if info_div:
            planes_element = info_div.find("div", string="Planes:")
            juicios_element = info_div.find("div", string="Juicios:")
            multas_element = info_div.find("div", string="Multas:")
            total_element = info_div.find("div", string="Total:")
            nombre_element = info_div.find("div", string="Nombre:")

            planes = planes_element.find_next_sibling("div").find('b').text.strip() if planes_element else "No disponible"
            juicios = juicios_element.find_next_sibling("div").find('b').text.strip() if juicios_element else "No disponible"
            multas = multas_element.find_next_sibling("div").find('b').text.strip() if multas_element else "No disponible"
            total = total_element.find_next_sibling("div").find('b').text.strip() if total_element else "No disponible"
            nombre = nombre_element.find_next_sibling("div").find('b').text.strip() if nombre_element else "No disponible"

            print("")
            print("Patente:", patente)
            print("Titular:", nombre)
            print("Planes:", planes)
            print("Juicios:", juicios)
            print("Multas:", multas) 
            print("Total deuda:", total)
        else:
            print("No se encontró la información deseada para la patente:", patente)
    finally:
        driver.quit()


#AGREGÁ LAS PATENTES QUE QUERES CONSULTAR ACÁ #
patentes = ["909KFZ", "GRL064"]

with ThreadPoolExecutor(max_workers=len(patentes)) as executor:
    executor.map(obtener_informacion_patente, patentes)
