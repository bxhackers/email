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
        e.g. Jack Cook <hello@jackcook.nyc>

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

    api_key = config.google_api_key
    spreadsheet_id = config.spreadsheet_id
    values = (spreadsheet_id, range_, api_key)

    r = requests.get("https://sheets.googleapis.com/v4/spreadsheets/%s/values/%s?key=%s" % values)
    members_json = r.json()["values"]

    # Remove the first row, since this just has column names
    members_json.pop(0)

    members = []

    for member_data in members_json:
        member = Member(member_data)
        members.append(member)

    return members
