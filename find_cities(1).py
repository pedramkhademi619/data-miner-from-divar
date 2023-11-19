import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
db = mysql.connector.connect(user = 'root', passwd = '13808472aA@#', host = 'localhost')
cursor = db.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS CITIES')
cursor.execute('USE CITIES')
cursor.execute('CREATE TABLE IF NOT EXISTS CITY_ (CITY VARCHAR(255))')
__response0 = requests.get(
    "https://worldpopulationreview.com/countries/cities/iran")
__soup0 = BeautifulSoup(__response0.text, "html.parser")
__cities = __soup0.find_all("td")
__cities = list(map(lambda x: str(x.text).lower(), __cities))
Cities = list(filter(lambda x: x == re.findall('[a-zA-Z]*', x)[0], __cities))

for city_ in Cities:
    cursor.execute("INSERT INTO CITY_ VALUES(%s)" % repr(city_))
db.commit()
db.close()
print('Successfull!')