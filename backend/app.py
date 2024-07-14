from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)
CORS(app)

@app.route('/api')
def get_data():

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        url = 'https://moj.ddor.rs/kupi-online/base/putno-osiguranje'
        driver.get(url)
        # Adatok gyűjtése Selenium segítségével
        data = []
        elements = driver.find_element(By.CLASS_NAME, 'header-title')
       
        print(elements)
           
        return jsonify(data)

    finally:
        # Ne felejtsd el lezárni a drivert, amikor végeztél vele
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
