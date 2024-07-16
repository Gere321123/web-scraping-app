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

def determine_age_group(age):
    if age < 18:
        return "do 18 godina"
    elif 18 <= age <= 69:
        return "18-70 godina"
    elif 70 <= age <= 79:
        return "70-80 godina"
    elif 80 <= age <= 84:
        return "80-85 godina"
    else:
        return "85+ godina"

def select_date(driver, date_picker_id, formatted_date):
    wait = WebDriverWait(driver, 10)
    
    date_picker = wait.until(EC.element_to_be_clickable((By.ID, date_picker_id)))
    date_picker.click()

    # Select the year
    year_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'picker__select--year')))
    year_options = year_select.find_elements(By.TAG_NAME, 'option')
    for option in year_options:
        if option.get_attribute('value') == formatted_date['year']:
            option.click()
            break

    # Select the month
    month_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'picker__select--month')))
    month_options = month_select.find_elements(By.TAG_NAME, 'option')
    for option in month_options:
        if option.text == formatted_date['month_name']:
            option.click()
            break

    # Select the day
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'picker__day')))
    days = driver.find_elements(By.CLASS_NAME, 'picker__day--infocus')
    for day in days:
        if day.text == formatted_date['day']:
            day.click()
            break

def get_travel_price_ddor(arrival_date, departure_date, ages, sport=None):
    formatted_arrival_date = format_date(arrival_date)
    formatted_departure_date = format_date(departure_date)

    service = Service(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = 'https://moj.ddor.rs/kupi-online/base/putno-osiguranje'
        driver.get(url)

        select_date(driver, 'mdb-datepicker-0', formatted_arrival_date)
        select_date(driver, 'mdb-datepicker-1', formatted_departure_date)

        wait = WebDriverWait(driver, 10)
        traveler_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'traveler-cnt-row')))

        for age in ages:
            age_group = determine_age_group(age)
            filtered_divs = []
            for div in traveler_divs:
                try:
                    age_div = div.find_element(By.XPATH, f".//div[text()='{age_group}']")
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
                print(f"No traveler divs found containing '{age_group}'.")
        
        if sport:
            select_sport(driver, sport)
        
        price_value = get_price(driver)
        return price_value

    finally:
        driver.quit()

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

def select_sport(driver, sport_name):
    wait = WebDriverWait(driver, 10)
    sport_select = wait.until(EC.element_to_be_clickable((By.ID, 'filter')))
    sport_select.click()
                
    sport_div = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{sport_name.strip()}')]")))
    sport_div.click()

def get_price(driver):
    wait = WebDriverWait(driver, 10)
    price_divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pack-text.price-div')))
    
    if price_divs:
        price_div = price_divs[0]
        price_value = price_div.text.strip()
        return price_value
    else:
        raise NoSuchElementException("Price div 'pack-text price-div' not found.")
