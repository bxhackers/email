import requests

class Member:
    first = ""
    last = ""
    email = ""

    def __init__(self, row):
        self.first = row[1]
        self.last = row[2]
        self.email = row[0]

    def __repr__(self):
        return "%s %s <%s>" % (self.first, self.last, self.email)

def request_members(keys):
    api_key = keys.google_api_key
    range_ = "A1:C1000"
    spreadsheet_id = keys.spreadsheet_id
    values = (spreadsheet_id, range_, api_key)

    r = requests.get("https://sheets.googleapis.com/v4/spreadsheets/%s/values/%s?key=%s" % values)
    members_json = r.json()["values"]
    members_json.pop(0)

    members = []

    for member_data in members_json:
        member = Member(member_data)
        members.append(member)

    return members
