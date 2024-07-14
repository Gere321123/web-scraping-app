import requests
from bs4 import BeautifulSoup

# URL, amit le szeretnél kérni
url = 'https://moj.ddor.rs/kupi-online/base/putno-osiguranje'

# Küldj HTTP GET kérést az URL-hez
response = requests.get(url)

# Ellenőrizd, hogy a kérés sikeres volt-e
if response.status_code == 200:
    # Parsing a HTML tartalmat BeautifulSoup segítségével
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Itt találsz meg egy példát arra, hogyan gyűjtsd be az adatokat
    # Ez csak egy példa, módosítsd az oldalszerkezet alapján
    data = []
    for item in soup.find_all('div', class_='example-class'):
        title = item.find('h2').text
        price = item.find('span', class_='price').text
        data.append({'title': title, 'price': price})
    
    # A kapott adatokat kiírjuk a konzolra
    print(data)
else:
    print(f'Failed to retrieve the page: {response.status_code}')
