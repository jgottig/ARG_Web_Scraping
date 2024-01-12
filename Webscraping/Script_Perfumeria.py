from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import csv
import requests
import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime


# Establezco el sitio web y la ruta del chromedriver
website = "https://www.preciosclaros.gob.ar/#!/buscar-productos"
chromedriver_path = "Insert your path to the chromedriver executable."


# Abro el sitio web y aprieto el botón Rosario
options = webdriver.ChromeOptions()
# Mantiene la sesión
options.add_experimental_option('detach', True)
options.add_argument("INSERTYOURPROFILE\\PerfilChrome")

# Especifico la ubicación del chromedriver directamente al crear la instancia del controlador
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(website)

wait= WebDriverWait(driver,10) #espera hasta 10 segundos como máximo, se usa con la dependencia EC

#Como guarda la sesión, después de la primera vez entra directo en Rosario entonces evitamos el error de no encontrarlo
try:
    rosario_button = wait.until(EC.element_to_be_clickable(driver.find_element(By.ID,"rosario")))
    rosario_button.click()
except:
    print("error")

#aca va a ir toda la info acumulada de los productos
data = []
pag = 0

#Path donde se va a guardar el CSV
#print(os.getcwd())

#ALMACEN tiene 97 Paginas
perfumeria_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/section/div[2]/section[1]/div[1]/div[11]/div/div/div/div[2]/div/h6')))
perfumeria_button.click()

s = 0

print("inicio" + str(datetime.now().time()))

while (s<62):
    for x in range (2,51):   #del 4 al 51 son los productos por página (2,3 min una página) --(almacen tiene 124 páginas)
        try:
            falla="En encontrar el artículo: " + str(x) + " de la pagina: " + str(pag)

            time.sleep(1)
            articulo = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/section/div[2]/section[2]/div/div[1]/article[2]/div[3]/div['+str(x)+']'))) #repetir, va a itinerar cambiando la X segun el rango a recorre (del 4 al 51)
            articulo = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/section/div[2]/section[2]/div/div[1]/article[2]/div[3]/div['+str(x)+']'))) #repetir, va a itinerar cambiando la X segun el rango a recorre (del 4 al 51)
            articulo.click()

            ##### HASTA ESTA PARTE, LLEGUE AL ARTICULO
            falla="En encontrar el nombre y su wait"
            
            nombreproducto = wait.until(EC.element_to_be_clickable((driver.find_element(By.XPATH, '//*[@id="detalle-producto-minorista"]/form/div/div/div[2]'))))
            nombreproducto = (nombreproducto).text[:-13]
            
            falla="En encontrar los otros campos del artículo"
            tablaprecios = driver.find_element(By.CLASS_NAME, 'table-responsive')   #me traigo la tabla entera ---QUIZAS SACAR
            thead = driver.find_element(By.TAG_NAME, 'thead')
            columns = [th.text for th in thead.find_elements(By.TAG_NAME, 'th')]   ##aca me traje los titulos de la tabla y los meti a una lista (sucursal, precio A, precio B, etc)
            columns.append("Nombre Del Articulo") # a esa lista le agrego una columna mas llamada nombre del articulo
            columns.append("Articulo + Pagina")
            print(columns)
            print(str(x))
            
            falla="En obtener la tabla del artículo"
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tbody = soup.find('tbody')
            
            for td in tbody.find_all('tr'):
                row = [str(i.text) for i in td.find_all('td')]
                row = [i.replace("\n", "") for i in row]
                row = [i.replace(" ", "") for i in row]
                row.append(nombreproducto)
                row.append("Articulo " + str(x) + " + Pagina " + str(pag + 1))
                row = [i.replace("\n", "") for i in row]
                data.append(row)
            falla="En el back"
            back=wait.until(EC.element_to_be_clickable(driver.find_element(By.CLASS_NAME,"fa")))
            back.click()
        except:
            print(falla)
    s = s + 1
    #Cuando termina de recorrer la página que suele ser hasta el 51 pero a veces menos y breakea el for, sigue con la siguiente
    try:
        time.sleep(3)
        pagina = driver.find_element(By.XPATH, '/html/body/main/div[2]/section/div[2]/section[2]/div/div[2]/ul/li[7]/a/span')
        pagina.click()
        pag=pag+1
        time.sleep(2)
    except:
        print("No puede pasar a la página "+ str(pag + 1) + " Damos por cerrado el proceso")
        break


#Emprolijar datos y exportar

nueva = []

for sublista in data:
    texto = sublista[0]
    texto_con_espacios = ''.join([' ' + letra if letra.isupper() else letra for letra in texto]).strip()
    sublista[0] = texto_con_espacios
    
    distancia = sublista[1]
    distancia = distancia.replace('kilómetros', '').replace('km', '').strip() + ' Kms'
    sublista[1] = distancia
    
    nueva.append(sublista)

df = pd.DataFrame(data=nueva, columns=columns)

df.to_csv("Perfumeria.csv", index = False)   ##### LO GUARDO EN .CSV en la misma carpeta q ya tengo este script para probar

print(df)

print("fin" + str(datetime.now().time()))