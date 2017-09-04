import boto3
import json
from pynliner import Pynliner
import requests

def get_keys():
    f = open("keys.json", "r")
    contents = f.read()
    f.close()

    return json.loads(contents)

def render_template():
    f = open("template.html", "r")
    html = f.read()
    f.close()

    f = open("template.css", "r")
    css = f.read()
    f.close()

    p = Pynliner().from_string(html).with_cssString(css)
    return p.run()

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

def request_members():
    keys = get_keys()
    api_key = keys["GOOGLE_API_KEY"]
    range_ = "A1:C1000"
    spreadsheet_id = keys["SPREADSHEET_ID"]
    values = (spreadsheet_id, range_, api_key)

    r = requests.get("https://sheets.googleapis.com/v4/spreadsheets/%s/values/%s?key=%s" % values)
    members_json = r.json()["values"]
    members_json.pop(0)

    members = []

    for member_data in members_json:
        member = Member(member_data)
        members.append(member)

    return members

client = boto3.client(service_name = "ses", region_name = "us-east-1")

source = "Bronx Science Hackers <jack@bxhackers.club>"

destination = {
    "ToAddresses": [
        "jack@bxhackers.club"
    ],
    "BccAddresses": [
        "hello@jackcook.nyc"
    ]
}

message = {
    "Subject": {
        "Data": "Testing"
    },
    "Body": {
        "Html": {
            "Data": render_template()
        }
    }
}

result = client.send_email(Source = source, Destination = destination, Message = message)
status_code = result["ResponseMetadata"]["HTTPStatusCode"]

if status_code == 200:
    print("Emails sent successfully!")
else:
    print("Emails could not be sent.")

print(result)
