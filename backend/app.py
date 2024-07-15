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

month_translation = {
    'January': 'Januar',
    'February': 'Februar',
    'March': 'Mart',
    'April': 'April',
    'May': 'Maj',
    'June': 'Jun',
    'July': 'Jul',
    'August': 'Avgust',
    'September': 'Septembar',
    'October': 'Oktobar',
    'November': 'Novembar',
    'December': 'Decembar'
}

def select_date(driver, date_picker_id, formatted_date):
    wait = WebDriverWait(driver, 10)
    
    date_picker = wait.until(EC.element_to_be_clickable((By.ID, date_picker_id)))
    date_picker.click()

    # Válasszuk ki az évet
    year_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'picker__select--year')))
    year_options = year_select.find_elements(By.TAG_NAME, 'option')
    for option in year_options:
        if option.get_attribute('value') == formatted_date['year']:
            option.click()
            break

    # Válasszuk ki a hónapot
    month_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'picker__select--month')))
    month_options = month_select.find_elements(By.TAG_NAME, 'option')
    for option in month_options:
        if option.text == formatted_date['month_name']:
            option.click()
            break

    # Válasszuk ki a napot
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'picker__day')))
    days = driver.find_elements(By.CLASS_NAME, 'picker__day--infocus')
    for day in days:
        if day.text == formatted_date['day']:
            day.click()
            break

@app.route('/api', methods=['POST'])
def get_data():
    
    
    data = request.json
    arrival_date = data.get('arrivalDate')
    departure_date = data.get('departureDate')
    age = data.get('age')


    # Érkezés dátum feldolgozása
    arrival_datetime = datetime.strptime(arrival_date, '%Y-%m-%d')
    arrival_month_name = arrival_datetime.strftime('%B')
    formatted_arrival_date = {
        'year': arrival_datetime.strftime('%Y'),
        'month': arrival_datetime.strftime('%m'),
        'month_name': month_translation[arrival_month_name],
        'day': arrival_datetime.strftime('%d')
    }

    # Távozás dátum feldolgozása
    departure_datetime = datetime.strptime(departure_date, '%Y-%m-%d')
    departure_month_name = departure_datetime.strftime('%B')
    formatted_departure_date = {
        'year': departure_datetime.strftime('%Y'),
        'month': departure_datetime.strftime('%m'),
        'month_name': month_translation[departure_month_name],
        'day': departure_datetime.strftime('%d')
    }
    print(formatted_departure_date['month_name'])


    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        url = 'https://moj.ddor.rs/kupi-online/base/putno-osiguranje'
        driver.get(url)

        select_date(driver, 'mdb-datepicker-0', formatted_arrival_date)
        select_date(driver, 'mdb-datepicker-1', formatted_departure_date)


        wait = WebDriverWait(driver, 10)
        traveler_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'traveler-cnt-row')))

        filtered_divs = []
        for div in traveler_divs:
            try:
                age_div = div.find_element(By.XPATH, ".//div[text()='18-70 godina']")
                filtered_divs.append(div)
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
            
        wait = WebDriverWait(driver, 10)    
        try:
            price_divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pack-text.price-div')))
            
            if price_divs:
                price_div = price_divs[0]

            price_value = price_div.text.strip()  
            # print(price_value)

            response_data = {'price': price_value}

        except NoSuchElementException:
            print("Price div 'pack-text price-div' not found.")

    finally:
        driver.quit()
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
