from selenium.webdriver.common.by import By
import time
from modules.utils import log_action_result, get_first_name, scroll_and_click_next, log_connection_result

def send_connect_requests(driver, message_template, max_requests):
    request_count = 0

    while request_count < max_requests:
        profile_blocks = driver.find_elements(By.XPATH, '//div[@class="entity-result__actions entity-result__divider"]/ancestor::li')

        if not profile_blocks:
            print("No profile blocks found.")
            return

        for profile in profile_blocks:
            if request_count >= max_requests:
                print(f"Reached the maximum number of requests: {max_requests}")
                return

            try:
                profile_name_element = profile.find_element(By.XPATH, './/span[@aria-hidden="true"]')
                if not profile_name_element:
                    continue
                profile_name = profile_name_element.text.strip()

                print(f"Checking profile: {profile_name}")

                # Look for Connect button
                try:
                    connect_button = profile.find_element(By.XPATH, './/span[@class="artdeco-button__text" and text()="Connect"]')
                    if connect_button:
                        connect_button.click()
                        time.sleep(2)
                    else:
                        print(f"Could not find Connect button for {profile_name}.")
                        log_action_result(profile_name, "Failed (No Connect button)")
                        continue
                except:
                    print(f"Could not find Connect button for {profile_name}. Skipping.")
                    log_action_result(profile_name, "Failed (No Connect button)")
                    continue

                # Try to find the "Add a note" button and send the message
                try:
                    add_note_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Add a note")]')
                    if add_note_button:
                        add_note_button.click()
                        time.sleep(1)

                        first_name = get_first_name(profile_name)
                        personalized_message = message_template.replace("{name}", first_name)

                        note_input = driver.find_element(By.XPATH, '//textarea[@name="message"]')
                        note_input.send_keys(personalized_message)
                except:
                    print(f"Couldn't find 'Add a note' button for {profile_name}. Proceeding without note.")

                # Find and click the "Send invitation" button
                send_button(driver, profile_name, request_count, max_requests)

            except Exception as e:
                print(f"Failed to process {profile_name}: {str(e)}")
                log_action_result(profile_name, f"Failed (Error: {str(e)})")
                continue
        
        scroll_and_click_next(driver)

def send_button(driver, profile_name, request_count, max_requests):
    
    # Find and click the "Send" button
    send_button = driver.find_element(By.XPATH, '//button//span[text()="Send"]')
    parent_send_button = send_button.find_element(By.XPATH, './ancestor::button')
    
    if parent_send_button and parent_send_button.is_enabled():
        parent_send_button.click()
        request_count += 1
        print(f"Request sent to {profile_name} successfully. ({request_count}/{max_requests})")
        log_connection_result(profile_name, "Success")
    else:
        # If "Send" button is disabled or not clickable, handle the case and close the modal
        close_button = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss"]')
        close_button.click()
        print(f"Couldn't send request to {profile_name}. Request not sent.")
        log_connection_result(profile_name, "Failed (No Send button)")