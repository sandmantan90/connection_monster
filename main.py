from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import yaml

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

USERNAME = config['username']
PASSWORD = config['password']
SEARCH_URL = config['search_url']
MESSAGE_TEMPLATE_PATH = config['message_template_path']

# Step 1: Load the message template from an external file
def load_message_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Step 2: Initialize the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Step 3: Open LinkedIn login page
driver.get('https://www.linkedin.com/login')

# Step 4: Manually enter the username and password into the login form
email_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')

# Input the username and password
email_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)

# Submit the login form
password_field.send_keys(u'\ue007')  # This simulates pressing "Enter"

# Wait for the login to complete
time.sleep(3)  # You can increase this if LinkedIn takes longer to load

# Step 5: Navigate to the LinkedIn search results page (enter manually or hard-code it)
driver.get(SEARCH_URL)

# Wait for the page to load fully
time.sleep(3)

# Step 6: Define the function to automate sending connection requests
def send_connection_requests(message_template):
    profile_blocks = driver.find_elements(By.XPATH, '//div[@class="entity-result__actions entity-result__divider"]/ancestor::li')

    if not profile_blocks:
        print("No profile blocks found.")
        return

    for profile in profile_blocks:
        try:
            profile_name_element = profile.find_element(By.XPATH, './/span[@aria-hidden="true"]')
            if not profile_name_element:
                continue
            profile_name = profile_name_element.text.strip()

            print(f"Checking profile: {profile_name}")

            # Check for Message button
            try:
                message_button = profile.find_element(By.XPATH, './/span[@class="artdeco-button__text" and text()="Message"]')
                if message_button:
                    print(f"{profile_name} - Message button found instead of Connect")
                    continue
            except:
                pass
            
            # Look for Connect button
            try:
                connect_button = profile.find_element(By.XPATH, './/span[@class="artdeco-button__text" and text()="Connect"]')
                if connect_button:
                    connect_button.click()
                    time.sleep(2)
                else:
                    print(f"Could not find Connect button for {profile_name}.")
                    continue
            except:
                print(f"Could not find Connect button for {profile_name}. Skipping.")
                continue

            # Try to find the "Add a note" button
            try:
                add_note_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Add a note")]')
                if add_note_button:
                    add_note_button.click()
                    time.sleep(1)
                    first_name = profile_name.split(' ')[0]
                    # Customize the message with the profile name
                    personalized_message = message_template.replace("{name}", first_name)

                    # Find the input field and enter the custom note
                    note_input = driver.find_element(By.XPATH, '//textarea[@name="message"]')
                    if note_input:
                        note_input.send_keys(personalized_message)
                    else:
                        print(f"Couldn't find note input field for {profile_name}. Sending request without note.")
            except:
                print(f"Couldn't find 'Add a note' button for {profile_name}. Proceeding without note.")

            # Find and click the "Send invitation" button
            send_button = driver.find_element(By.XPATH, '//button//span[text()="Send"]')
            parent_send_button = send_button.find_element(By.XPATH, './ancestor::button')
            
            if parent_send_button:
                parent_send_button.click()
                print(f"Connection request sent to {profile_name} successfully.")
            else:
                print(f"Couldn't find Send button for {profile_name}. Request may not have been sent.")

            # Pause to avoid triggering LinkedIn's rate-limiting
            time.sleep(3)

        except Exception as e:
            print(f"Failed to process {profile_name}: {str(e)}")
            continue

# Step 7: Load the message template from the external file
message_template = load_message_template(MESSAGE_TEMPLATE_PATH)

# Step 8: Call the function to send connection requests
send_connection_requests(message_template)

# Optional: Close the browser when finished
driver.quit()