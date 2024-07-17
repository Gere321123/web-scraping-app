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

month_translation = {
    'January': 'januar',
    'February': 'februar',
    'March': 'mart',
    'April': 'april',
    'May': 'maj',
    'June': 'jun',
    'July': 'jul',
    'August': 'avgust',
    'September': 'septembar',
    'October': 'oktobar',
    'November': 'novembar',
    'December': 'decembar'
}
def format_date(date_str):
    date_time = datetime.strptime(date_str, '%Y-%m-%d')
    month_name = date_time.strftime('%B')
    formatted_date = {
        'year': date_time.strftime('%Y'),
        'month': date_time.strftime('%m'),
        'month_name': month_translation[month_name],
        'day': date_time.strftime('%d')
    }
    return formatted_date

def select_date(driver, date_picker_id, formatted_date):
    wait = WebDriverWait(driver, 10)
    
    date_picker = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, date_picker_id)))
    date_picker.click()

     # Kattintsunk az első gombra, amelynek az osztálya 'current'
    year_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.current")))
    year_button.click()

    year_span = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[@role='gridcell']/span[text()='{formatted_date['year']}']")))
    year_span.click()

    month_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@role='grid' and @class='months']/tbody//span[text()='jul']")))
    month_span.click()

    # Kattintás a napra
    day_span = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[@role='gridcell']/span[text()='{formatted_date['day']}']")))
    day_span.click()
    
    time.sleep(21)

    # Válaszd ki a napot
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'picker__day')))
    days = driver.find_elements(By.CLASS_NAME, 'picker__day--infocus')
    for day in days:
        if day.text == formatted_date['day']:
            day.click()
            break

def get_travel_price_etigrav(arrival_date, departure_date, ages):
    formatted_arrival_date = format_date(arrival_date)
    formatted_departure_date = format_date(departure_date)

    options = Options()
    options.headless = True
    options.add_argument('--start-maximized')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = 'https://e.triglav.rs/putno-osiguranje/putno-osiguranje?gad_source=1'
        driver.get(url)

        select_date(driver, 'mobileDate', formatted_arrival_date)
        select_date(driver, 'marginRight10', formatted_departure_date)
        
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'basicPrice')))
        basic_price = element.text.strip()  # Strip to remove any surrounding whitespace

        return basic_price

    finally:
        driver.quit()
