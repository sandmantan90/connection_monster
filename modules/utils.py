import yaml
import time
import os
from selenium.webdriver.common.by import By

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def load_message_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def log_action_result(profile_name, status):
    with open('logs/action_log.txt', 'a') as log_file:
        log_file.write(f"{profile_name}: {status}\n")

def get_first_name(profile_name):
    if '(' in profile_name and ')' in profile_name:
        first_name = profile_name.split('(')[1].split(')')[0].strip()
    else:
        first_name = profile_name.split(' ')[0].strip()
    return first_name

def scroll_and_click_next(driver):
    time.sleep(2)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*.9);")
        time.sleep(2)
        next_button = driver.find_element(By.XPATH, '//span[text()="Next"]/ancestor::button')
        if "artdeco-button--disabled" in next_button.get_attribute("class"):
            print("Next button is disabled. Ran out of options.")
            return
        else:
            print("Clicking Next to go to the next page...")
            next_button.click()
            time.sleep(5)  # Wait for the next page to load
    except Exception as e:
        print(f"Could not find or click Next button: {str(e)}")


def log_connection_result(profile_name, status):
    # Create the 'logs' directory if it doesn't exist
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Open the log file in append mode to log results
    log_file_path = os.path.join(log_directory, 'connection_log.txt')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{profile_name}: {status}\n")

    print(f"Logged result for {profile_name}: {status}")
