import requests

class Member:
    """A model representing a member of the club.

    Attributes:
        first: The member's first name.
        last: The member's last name.
        email: The member's email address.
    """

    def __init__(self, row):
        """Creates a member model from a row in the Google Sheet.

        Args:
            row: The row of the spreadsheet that represents this member.
        """

        self.first = row[1]
        self.last = row[2]
        self.email = row[0]

    def __repr__(self):
        """Returns a string that can be used in a to/cc/bcc field in an email.
        e.g. Jack Cook <jack@bxhackers.club>

        Returns:
            The string representing this member.
        """

        return "%s %s <%s>" % (self.first, self.last, self.email)

def request_members(config):
    """Requests all members from the Google Sheet.

    Args:
        config: The config model that was generated from config.json.

    Returns:
        An array of all members in the Google Sheet.
    """

    # 1000 is arbitrary since there doesn't seem to be a "last row" selector.
    #
    # Choosing a value that is greater than the number of rows in your
    # spreadsheet causes no issues, so just pick a bigger number if necessary.
    range_ = "A1:C1000"

    api_key = config.keys.google_api_key

    if api_key == None or api_key == "":
        print("Your API key was entered incorrectly in config.json. You can generate a key at https://console.developers.google.com/apis/credentials")
        return None

    spreadsheet_id = config.keys.spreadsheet_id

    if spreadsheet_id == None or spreadsheet_id == "":
        print("Your spreadsheet id was entered incorrectly in config.json. You can find your spreadsheet id in your Google Sheet's URL, e.g. https://docs.google.com/spreadsheets/u/1/d/{SPREADSHEET_ID_IS_HERE}/edit")
        return None

    values = (spreadsheet_id, range_, api_key)

    r = requests.get("https://sheets.googleapis.com/v4/spreadsheets/%s/values/%s?key=%s" % values)
    json = r.json()
    members_json = None

    if "values" in json:
        members_json = json["values"]
    else:
        print("There was an issue retrieving data from your Google Sheet. Make sure that your spreadsheet_id is correct in config.json.")
        return None

    # Remove the first row since this just has column names
    members_json.pop(0)

    members = []

    for member_data in members_json:
        member = Member(member_data)
        members.append(member)

    return members
