import json

class Config:
    """A model representing the config.json file.

    Attributes:
        email: The model representing the email section of this config file.
        keys: The model representing the keys section of this config file.
    """

    def __init__(self, contents):
        """Creates a config model from the contents of the config.json file.

        Args:
            contents: The contents of the config.json file.
        """

        data = json.loads(contents)
        self.email = EmailConfig(data["email"])
        self.keys = KeysConfig(data["keys"])

class EmailConfig:
    """A model representing the email section of the config.json file.

    Attributes:
        recipient_email: The email address of the recipient of your emails.
        recipient_name: The name of the recipient of your emails.
        sender_email: The email address of the sender of your emails.
        sender_name: The name of the sender of your emails.
    """

    def __init__(self, data):
        """Creates an email config model from the dictionary retrieved from
        the config.json file.

        Args:
            data: The email dictionary retrieved from config.json.
        """

        self.recipient_email = data["recipient_email"]
        self.recipient_name = data["recipient_name"]
        self.sender_email = data["sender_email"]
        self.sender_name = data["sender_name"]

class KeysConfig:
    """A model representing the keys section of the config.json file.

    Attributes:
        google_api_key: The Google API key used in requests to Google Sheets.
        spreadsheet_id: The ID of the Google Sheet being used to store emails.
    """

    def __init__(self, data):
        """Creates a keys config model from the dictionary retrieved from the
        config.json file.

        Args:
            data: The keys dictionary retrieved from config.json.
        """

        self.google_api_key = data["google_api_key"]
        self.spreadsheet_id = data["spreadsheet_id"]

def load_config():
    """Loads the config model from the config.json file.

    Returns:
        The config model that was retrieved.
    """

    f = open("config.json", "r")
    contents = f.read()
    f.close()

    return Config(contents)
