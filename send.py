import boto3
import sys

from src import *

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
keys = load_keys()

for member in request_members(keys):
    result = send_email(client, email, member)

    status_code = result["ResponseMetadata"]["HTTPStatusCode"]

    if status_code == 200:
        print("Email to %s was sent successfully!" % member.email)
    else:
        print("Email to %s could not be sent." % member.email)
        print(result)
