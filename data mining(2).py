import requests
from bs4 import BeautifulSoup
import re
import mysql.connector

db = mysql.connector.connect(user = 'root', passwd = '13808472aA@#', host = '127.0.0.1', database = 'CITIES')
cursor = db.cursor()
cursor.execute('SELECT * FROM CITY_')
cities = cursor.fetchall()
cities = list(map(lambda x:x[0], cities))

def link_miner(city):
    response = requests.get('https://divar.ir/s/%s/auto' % city)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [link.get('href') for link in soup.find_all('a')][19:-1]
    return links


def data_miner(sublink):
    response = requests.get(f'https://divar.ir{sublink}')
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        name = soup.find_all(
            "h1", class_="kt-page-title__title kt-page-title__title--responsive-sized")[0].text
        name = re.findall('(.*)،', name)[0]
        milage = int(soup.find_all(
            "span", class_="kt-group-row-item__value")[0].text.replace('٬', ''))
        try:
            model = int(soup.find_all(
                "span", class_="kt-group-row-item__value")[1].text)
        except ValueError:
            model = soup.find_all(
                "span", class_="kt-group-row-item__value")[1].text
        engine_status = soup.find_all(
            "p", class_="kt-unexpandable-row__value")[0].text
        chassis_status = soup.find_all(
            "p", class_="kt-unexpandable-row__value")[1].text
        body_status = soup.find_all(
            "p", class_="kt-unexpandable-row__value")[2].text
        insurance = soup.find_all(
            "p", class_="kt-unexpandable-row__value")[3].text
        gearbox = soup.find_all(
            "p", class_="kt-unexpandable-row__value")[4].text
        try:
            price = int(soup.find_all(
                "p", class_="kt-unexpandable-row__value")[6].text.replace('٬', '')[:-6])
        except ValueError:
            price = soup.find_all(
                "p", class_="kt-unexpandable-row__value")[6].text
        return name, milage, model, engine_status, chassis_status, body_status, insurance, gearbox, price
    except IndexError:
        return None

data = []
for city in cities:
    print(city.title())
    for sublink in link_miner(city):
        if data_miner(sublink) != None:
            data.append(data_miner(sublink))
    print(f'The information of {city.title()} city is successfully mined.')
cursor.execute('CREATE DATABASE IF NOT EXISTS INFORMATION')
cursor.execute('USE INFORMATION')
cursor.execute('CREATE TABLE IF NOT EXISTS CAR(name VARCHAR(255), milage VARCHAR(255), model VARCHAR(255), engine_status VARCHAR(255), chassis_status VARCHAR(255), body_status VARCHAR(255), insurance VARCHAR(255), gearbos VARCHAR(255), price VARCHAR(255))')
for i in set(data):
    cursor.execute(f'INSERT INTO CAR VALUES({repr(i[0])}, {repr(i[1])}, {repr(i[2])}, {repr(i[3])}, {repr(i[4])}, {repr(i[5])}, {repr(i[6])}, {repr(i[7])}, {repr(i[8])})')
    db.commit()
    
db.close()

