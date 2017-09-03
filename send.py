import boto3
import pynliner

def render_template():
    f = open("template.html", "r")
    contents = f.read()
    f.close()

    return pynliner.fromString(contents)

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
