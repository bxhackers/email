import boto3
import sys

from src import *

def send_email(client, email, member):
    """Sends an email to someone.

    Args:
        client: The boto3 client that will make the request to AWS.
        email: The model of the email that should be sent.
        member: The member that this email will be sent to.

    Returns:
        The JSON response of the request that was made to send the email.
    """

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
            "Data": email.subject
        },
        "Body": {
            "Html": {
                "Data": render_template(email, member)
            }
        }
    }

    return client.send_email(Source = source, Destination = destination, Message = message)

# Remove .email extension if it's here in case it was added mistakenly
email_name = sys.argv[1].replace(".email", "")

client = boto3.client(service_name = "ses", region_name = "us-east-1")
email = load_email(email_name)
keys = load_keys()

for member in request_members(keys):
    result = send_email(client, email, member)

    status_code = result["ResponseMetadata"]["HTTPStatusCode"]

    if status_code == 200:
        print("Email to %s was sent successfully!" % member.email)
    else:
        print("Email to %s could not be sent." % member.email)
        print(result)
