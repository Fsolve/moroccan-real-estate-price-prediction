import requests
from fake_useragent import UserAgent
import time
import random
from bs4 import BeautifulSoup
import csv
import os
# Initialize a session and UserAgent
session = requests.Session()
ua = UserAgent()

# Set up the URL
base_url = "https://www.avito.ma/fr/maroc/maisons-%C3%A0_vendre?o="
headers = {
            "User-Agent": ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.avito.ma"
        }


#

# Make a request to the website


for j in range(1,352):
    response = session.get(base_url+str(j), headers=headers)
    htmlData = response.content
    parsedData = BeautifulSoup(htmlData, "html.parser")
    info = parsedData.find_all('div', class_="sc-b57yxx-1 kBlnTB")

    # Créer ou ouvrir le fichier CSV en mode append (ajouter des lignes à la fin du fichier)
    with open('data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(len(info)):
            class_chambres = info[i].find("div", title="Chambres")
            chambres = class_chambres.find('span').get_text() if class_chambres and class_chambres.find(
                'span') else 'null'

            class_saleBain = info[i].find("div", title="Salle de bain")
            salles_de_bain = class_saleBain.find('span').get_text() if class_saleBain and class_saleBain.find(
                'span') else 'null'

            class_superficie = info[i].find("div", title="Surface totale")
            superficie = class_superficie.find('span').get_text() if class_superficie and class_superficie.find(
                'span') else 'null'

            prix = info[i].find('span', dir="auto").get_text() if info[i].find('span', dir="auto") else 'null'

            ville = info[i].find('p', class_="sc-1x0vz2r-0 iFQpLP").get_text() if info[i].find('p',
                                                                                               class_="sc-1x0vz2r-0 iFQpLP") else 'null'

            title = info[i].find('p', class_="sc-1x0vz2r-0 czqClV").get_text() if info[i].find('p',
                                                                                               class_="sc-1x0vz2r-0 czqClV") else 'null'

            # print("chambres : ", chambres, " sale_de_bain ", salles_de_bain, " superficie ", superficie, " price ",
            #       prix,
            #       " location ", ville, " title ", title)

            writer.writerow([chambres, salles_de_bain, superficie, prix, ville, title, 'Maison et Villa'])

    print(j)