import boto3
import json
from pynliner import Pynliner

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
