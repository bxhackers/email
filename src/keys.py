import json

class Keys:
    """A model representing the keys.json file.

    Attributes:
        google_api_key: The Google API key used in requests to Google Sheets.
        spreadsheet_id: The ID of the Google Sheet being used to store emails.
    """

    def __init__(self, contents):
        """Creates a keys file model from the contents of the keys.json file.

        Args:
            contents: The contents of the keys.json file.
        """

        data = json.loads(contents)
        self.google_api_key = data["GOOGLE_API_KEY"]
        self.spreadsheet_id = data["SPREADSHEET_ID"]

def load_keys():
    """Loads the keys file model from the keys.json file.

    Returns:
        The keys file model that was retrieved.
    """

    f = open("keys.json", "r")
    contents = f.read()
    f.close()

    return Keys(contents)
