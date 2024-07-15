from flask import Flask,request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def get_data():
    
    data = request.json
    arrival_date = data.get('arrivalDate')
    departure_date = data.get('departureDate')
    age = data.get('age')
    formatted_arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').strftime('%d.%m.%Y')
    formatted_departure_date = datetime.strptime(departure_date, '%Y-%m-%d').strftime('%d.%m.%Y')
    print(formatted_arrival_date)

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        url = 'https://moj.ddor.rs/kupi-online/base/putno-osiguranje'
        driver.get(url)
        # Adatok gyűjtése Selenium segítségével
        data = []
        # input = driver.find_element(By.CLASS_NAME, 'traveler-cnt-input ng-tns-c180-1 ng-pristine ng-valid ng-touched')
        # input.send_keys(1)
        # time.sleep(3)
        
        wait = WebDriverWait(driver, 10)
        date_picker = wait.until(EC.element_to_be_clickable((By.ID, 'mdb-datepicker-0')))
        date_picker.click()

        # Wait for the date picker to become visible
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'picker__day')))

        # Find the correct td element containing the div with text '20'
        days = driver.find_elements(By.CLASS_NAME, 'picker__day--infocus')
        for day in days:
            if '20' in day.text:
                day.click()
                break
            
        date_picker = wait.until(EC.element_to_be_clickable((By.ID, 'mdb-datepicker-1')))
        date_picker.click()

        # Wait for the date picker to become visible
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'picker__day')))

        # Find the correct td element containing the div with text '20'
        days = driver.find_elements(By.CLASS_NAME, 'picker__day--infocus')
        for day in days:
            if '25' in day.text:
                day.click()
                break


        wait = WebDriverWait(driver, 10)
        traveler_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'traveler-cnt-row')))

        filtered_divs = []
        for div in traveler_divs:
            try:
                age_div = div.find_element(By.XPATH, ".//div[text()='18-70 godina']")
                filtered_divs.append(div)
                print(div)
            except NoSuchElementException:
                continue
    
        if filtered_divs:
            for div in filtered_divs:
                try:
                    label = div.find_element(By.CLASS_NAME, "fas.fa-plus")
                    label.click()
                except NoSuchElementException:
                    print("Sibling div 'travel-cnt-div' not found.")
        else:
            print("No traveler divs found containing '18-70 godina'.")
            
            
        time.sleep(10)
           
        return jsonify(data)

    finally:
        # Ne felejtsd el lezárni a drivert, amikor végeztél vele
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
