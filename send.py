import boto3
import json
from pynliner import Pynliner
import requests
import sys

class Email:
    subject = ""
    text = ""

    def __init__(self, contents):
        lines = contents.split("\n")
        self.subject = lines[0]

        text = ""

        for line in lines[2:-1]:
            text += "%s\n" % line

        self.text = text

def load_email(name):
    f = open("./emails/%s.email" % name)
    contents = f.read()
    f.close()

    email = Email(contents)
    return email

def get_keys():
    f = open("keys.json", "r")
    contents = f.read()
    f.close()

    return json.loads(contents)

def render_template(email, member):
    f = open("template.html", "r")
    html = f.read()
    f.close()

    text = ""

    for line in email.text.split("\n"):
        text += "<p>%s</p>" % line

    html = html.replace("{{name}}", member.first).replace("{{content}}", text)

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

def send_email(client, email, member):
    source = "Bronx Science Hackers <jack@bxhackers.club>"

    destination = {
        "ToAddresses": [
            "Jack Cook <jack@bxhackers.club>"
        ],
        "BccAddresses": [
            "%s %s <%s>" % (member.first, member.last, member.email)
        ]
    }

    message = {
        "Subject": {
            "Data": "Testing 1"
        },
        "Body": {
            "Html": {
                "Data": render_template(email, member)
            }
        }
    }

    return client.send_email(Source = source, Destination = destination, Message = message)

client = boto3.client(service_name = "ses", region_name = "us-east-1")
email = load_email(sys.argv[1])

for member in request_members():
    result = send_email(client, email, member)

    status_code = result["ResponseMetadata"]["HTTPStatusCode"]

    if status_code == 200:
        print("Email to %s was sent successfully!" % member.email)
    else:
        print("Email to %s could not be sent." % member.email)
        print(result)
