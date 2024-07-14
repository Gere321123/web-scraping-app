from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api')
def get_data():
    url = 'https://moj.ddor.rs/kupi-online/base/putno-osiguranje'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = []
        for item in soup.find_all('div', class_='dates-info ng-tns-c180-1'):
            title = item.find('h2').text
            price = item.find('span', class_='price').text
            data.append({'title': title, 'price': price})
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to retrieve the page'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
