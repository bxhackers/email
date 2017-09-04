import json

class Keys:
    google_api_key = ""
    spreadsheet_id = ""

    def __init__(self, contents):
        data = json.loads(contents)
        self.google_api_key = data["GOOGLE_API_KEY"]
        self.spreadsheet_id = data["SPREADSHEET_ID"]

def load_keys():
    f = open("keys.json", "r")
    contents = f.read()
    f.close()

    return Keys(contents)
