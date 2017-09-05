import json

class Config:
    """A model representing the config.json file.

    Attributes:
        google_api_key: The Google API key used in requests to Google Sheets.
        spreadsheet_id: The ID of the Google Sheet being used to store emails.
    """

    def __init__(self, contents):
        """Creates a config model from the contents of the config.json file.

        Args:
            contents: The contents of the config.json file.
        """

        data = json.loads(contents)
        self.google_api_key = data["GOOGLE_API_KEY"]
        self.spreadsheet_id = data["SPREADSHEET_ID"]

def load_config():
    """Loads the config model from the config.json file.

    Returns:
        The config model that was retrieved.
    """

    f = open("config.json", "r")
    contents = f.read()
    f.close()

    return Config(contents)
