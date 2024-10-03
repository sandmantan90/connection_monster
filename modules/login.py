from selenium.webdriver.common.by import By
import time

def login_to_linkedin(driver, username, password):
    driver.get('https://www.linkedin.com/login')
    
    # Find the username and password fields
    email_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')

    # Input the username and password
    email_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(u'\ue007')  # This simulates pressing "Enter"
    
    # Wait for login to complete
    time.sleep(3)