
# Connection Monster

This Python-based LinkedIn Automation Tool enables users to send personalized connection or message requests automatically, based on the action defined in the configuration. It uses the Selenium library to interact with LinkedIn's web interface and allows for configurable actions.

## Features
- **Automated Connection Requests:** Send personalized connection requests using a pre-defined message template.
- **Automated Messages:** Send custom messages to existing connections.
- **File Attachments:** Attach files to the message when sending personalized requests.
- **Logging:** Keep track of successful and failed connection attempts.
- **Next Page Navigation:** Automatically navigate through LinkedIn search result pages.

## Project Structure

```
├── content
│   ├── connect_message.txt           # Message template for connection requests
│   ├── referral_request_message.txt  # Message template for referrals or direct messages
│   ├── resume.pdf                    # Sample file to attach in messages
├── modules
│   ├── __pycache__                   # Cached Python bytecode files (ignore this)
│   ├── connect.py                    # Module for handling connection requests
│   ├── login.py                      # Module for logging into LinkedIn
│   ├── message.py                    # Module for handling message sending logic
│   ├── utils.py                      # Utility functions used by the main program
├── .gitignore                        # Ignored files (including pycache)
├── LICENSE                           # License information
├── main.py                           # Main script to run the automation
```

## Requirements

- Python 3.6+
- `selenium`
- `webdriver_manager`
- `PyYAML`

You can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Setup and Configuration

### Step 1: Install WebDriver and Required Libraries

Install the necessary Python packages:

```bash
pip install selenium webdriver-manager pyyaml
```

### Step 2: Configure the YAML File

In the root directory, create a `config.yaml` file to configure your LinkedIn credentials, message templates, and the maximum number of requests.

Example `config.yaml`:

```yaml
username: "your_linkedin_email"
password: "your_linkedin_password"
search_url: "https://www.linkedin.com/search/results/people/?keywords=python"
message_template_path: "content/connect_message.txt"
max_requests: 10
action: "connect"  # Options: 'connect' or 'message'
```

### Step 3: Add Message Templates

Store your personalized message templates in the `content` directory.

- **connect_message.txt**: Template used for connection requests. You can include `{name}` in the template, which will be replaced with the recipient's first name.
- **referral_request_message.txt**: Template used for sending direct messages.

### Step 4: Running the Automation

To run the automation tool, execute the `main.py` file:

```bash
python main.py
```

Based on the action defined in your `config.yaml` file (either "connect" or "message"), the script will either:
- Send connection requests using the `connect.py` module.
- Send messages to existing connections using the `message.py` module.

## How It Works

1. **Login**: The `login.py` script handles the login process to LinkedIn.
2. **Action Handling**: Based on the configured action in the `config.yaml` file:
   - If the action is `connect`, the `connect.py` module handles connection requests.
   - If the action is `message`, the `message.py` module handles sending messages.
3. **Logging**: Results of the automation (success/failure) are logged in the `logs/connection_log.txt` file.

## Logging Considerations

If the `logs/` directory doesn't already exist, you will need to create it manually to ensure that logging works properly. Alternatively, modify the script to create the folder automatically.

## Security Considerations

The password is currently stored in plain text in `config.yaml` for simplicity. For improved security in production environments, consider:
- Storing credentials in environment variables.
- Using a secure storage solution like AWS Secrets Manager or Azure Key Vault.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request for any changes or improvements.

## Issues

For any issues, feel free to open a new issue on GitHub. We appreciate your feedback and contributions!
