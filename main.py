from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from modules.login import login_to_linkedin
from modules.connect import send_connect_requests
#from modules.message import send_message_requests
from modules.utils import load_config, load_message_template

def main():
    # Load the configuration and message template
    config = load_config('config.yaml')
    message_template = load_message_template(config['message_template_path'])

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Login to LinkedIn
    login_to_linkedin(driver, config['username'], config['password'])

    # Navigate to the LinkedIn search results page
    driver.get(config['search_url'])
    time.sleep(3)  # Wait for the page to load fully

    # Perform actions based on mode (either "connect" or "message")
    if config['mode'] == "connect":
        send_connect_requests(driver, message_template, config['max_requests'])
    #elif config['mode'] == "message":
        #send_message_requests(driver, message_template, config['max_requests'])

    # Close the browser when done
    driver.quit()

if __name__ == "__main__":
    main()
