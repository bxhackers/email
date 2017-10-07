import argparse
import boto3
import sys

from src import *

def send_email(client, config, email, member = None, recipients = None):
    """Sends an email to someone. Either member or recipients must not be None.

    Args:
        client: The boto3 client that will make the request to AWS.
        config: The current config file model.
        email: The model of the email that should be sent.
        member: The member that this email will be sent to.
        recipients: An array of email addresses that this email should be sent to.

    Returns:
        The JSON response of the request that was made to send the email.
    """

    if member == None and recipients == None:
        print("Error: either member or recipients must be specified")
        return
    elif member != None and recipients != None:
        print("Error: both member or recipients was specified. only one is needed")
        return

    source = "%s <%s>" % (config.email.sender_name, config.email.sender_email)
    destination = {}

    if member is not None:
        destination = {
            "ToAddresses": [
                "%s <%s>" % (config.email.recipient_name, config.email.recipient_email)
            ],
            "BccAddresses": [
                "%s %s <%s>" % (member.first, member.last, member.email)
            ]
        }
    else:
        destination = {
            "ToAddresses": [
                "%s <%s>" % (config.email.recipient_name, config.email.recipient_email)
            ],
            "BccAddresses": recipients
        }

    message = {
        "Subject": {
            "Data": email.subject
        },
        "Body": {
            "Html": {
                "Data": render_template(email, member)
            },
            "Text": {
                "Data": render_template_text(email, member)
            }
        }
    }

    return client.send_email(Source = source, Destination = destination, Message = message)

parser = argparse.ArgumentParser(description = "Send emails with style.")
parser.add_argument("email", type = str, help = "The name of the email that you want to send out.")
args = parser.parse_args()

# Remove .email extension if it's here in case it was added mistakenly
email_name = args.email.replace(".email", "")

client = boto3.client(service_name = "ses", region_name = "us-east-1")
email = load_email(email_name)

# Exit if there was an error loading the email model
if email == None:
    sys.exit(0)

config = load_config()
members = request_members(config)

# Exit if there was an error loading members
if members == None:
    sys.exit(0)

# Use "person" if sending emails to one person, otherwise use "people"
people = "person" if len(members) == 1 else "people"

# Make sure that the user is sure of what they're doing
print("You are about to send \"%s\" to %d %s." % (email.subject, len(members), people))
response = input("Do you want to continue? [Y/n] ")

# Accept empty string, Y, and y as confirmation, otherwise do not send emails
if response not in ["", "Y", "y"]:
    print("Abort.")
    sys.exit(0)

if contains_variables(email):
    for member in members:
        result = send_email(client, config, email, member)

        status_code = result["ResponseMetadata"]["HTTPStatusCode"]

        if status_code == 200:
            print("Email to %s was sent successfully!" % member.email)
        else:
            print("Email to %s could not be sent." % member.email)
            print(result)
else:
    recipients = []

    for member in members:
        recipients.append(str(member))

    result = send_email(client, config, email, recipients = recipients)
    status_code = result["ResponseMetadata"]["HTTPStatusCode"]

    if status_code == 200:
        print("Email was sent out successfully!")
    else:
        print("Email could not be sent.")
        print(result)
