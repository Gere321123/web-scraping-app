from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def format_date(date_str):
    date_time = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = f"{date_time.strftime('%d')}.{date_time.strftime('%m')}.{date_time.strftime('%Y')}"
    return formatted_date

def select_date(driver, date_picker_id, formatted_date):
    wait = WebDriverWait(driver, 10)
    
    date_picker = wait.until(EC.element_to_be_clickable((By.ID, date_picker_id)))
    date_picker.clear()
    date_picker.send_keys(formatted_date)
    date_picker.send_keys("\n")  # Sometimes a newline character is needed to confirm the input

def get_travel_price_sava(arrival_date, departure_date, ages):
    formatted_arrival_date = format_date(arrival_date)
    formatted_departure_date = format_date(departure_date)

    options = Options()
    options.headless = True
    options.add_argument('--start-maximized')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = 'https://webshop.sava-osiguranje.rs/putno-osiguranje/?gad_source=1'
        driver.get(url)

        select_date(driver, 'startDate', formatted_arrival_date)
        select_date(driver, 'endDate', formatted_departure_date)
        
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'basicPrice')))
        basic_price = element.text.strip()  # Strip to remove any surrounding whitespace

        return basic_price

    finally:
        driver.quit()
