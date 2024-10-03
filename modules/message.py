from selenium.webdriver.common.by import By
import time
from modules.utils import log_action_result, get_first_name, scroll_and_click_next

def send_message_requests(driver, message_template, max_requests):
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

                # Look for Message button
                try:
                    message_button = profile.find_element(By.XPATH, './/span[@class="artdeco-button__text" and text()="Message"]')
                    if message_button:
                        message_button.click()
                        time.sleep(2)

                        active_element = driver.switch_to.active_element
                        
                        first_name = get_first_name(profile_name)
                        personalized_message = message_template.replace("{name}", first_name)
                        active_element.send_keys(personalized_message)
                        attach_resume_directly(driver, profile_name)
                        send_button(driver, profile_name, request_count, max_requests)
                        close_button(driver)
                    else:
                        print(f"Could not find Message button for {profile_name}.")
                        log_action_result(profile_name, "Failed (No Message button)")
                        continue
                except:
                    print(f"Could not find Message button for {profile_name}. Skipping.")
                    log_action_result(profile_name, "Failed (No Message button)")

            except Exception as e:
                print(f"Failed to process {profile_name}: {str(e)}")
                log_action_result(profile_name, f"Failed (Error: {str(e)})")
                continue
        
        scroll_and_click_next(driver)

def send_button(driver, profile_name, request_count, max_requests):
    # Find and click the "Send" button
    send_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    try:
        send_button = send_button.find_element(By.XPATH, './ancestor::button')
    except:
        pass
    if send_button and send_button.is_enabled():
        send_button.click()
        request_count += 1
        print(f"Message sent to {profile_name} successfully. ({request_count}/{max_requests})")
        log_action_result(profile_name, "Success")
    else:
        print(f"Couldn't find Send button for {profile_name}. Message may not have been sent.")
        log_action_result(profile_name, "Failed (No Send button)")

def close_button(driver):
    # Find and click the "Send" button
    close_button = driver.find_element(By.XPATH, '//*[starts-with(@class, "msg-overlay-bubble-header__control art")]')
    
    if close_button and close_button.is_enabled():
        close_button.click()
        
        

def attach_resume_directly(driver, profile_name):
    try:
        # Find the file input element by its type
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_path = r"C:\Users\admin\Desktop\Ketan's Files\PersonalProjects\Referal Monster\connection_monster\content\resume.pdf"
        # Send the file path to upload the file directly
        file_input.send_keys(file_path)  # This uploads the file automatically
        
        print(f"File attached successfully for {profile_name}")
    
    except Exception as e:
        print(f"Error while attaching the file for {profile_name}: {e}")
