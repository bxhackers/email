# atomhacks/email

This is what we use to send emails out to everyone in Bronx Science Hackers. It has only been tested on macOS, but in theory this should work in Linux environments as well.


## Setup

First, make sure you have Python 3.6 and pip installed. After that, run the following command to install all dependencies:

```bash
$ pip install -r requirements.txt
```

After installing all necessary requirements, you'll need to verify that you're authenticated with AWS. We use `boto3` for AWS requests, so refer to the [Boto 3 documentation](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration) to figure out how to get yourself set up. You should make sure that your credentials are configured to work with [Amazon SES](https://aws.amazon.com/ses/).

## Usage

1. **Create a spreadsheet with emails you want to use**

`email` reads names and email addresses from a Google Spreadsheet, which many clubs already use to manage data about their members. You'll need to set one up where the first column is of email addresses, the second column is first names, and the third column is last names. The spreadsheet also must be set to the sharing setting where anyone who has the link can view it. [Here](https://docs.google.com/spreadsheets/d/1luDE6PCo2CCBuQAF51bfig9GACMSBQh1c6oX9aw3n64/edit?usp=sharing) is an example of one that would work.

2. **Save your spreadsheet's ID**

Once you have created your spreadsheet, look at the URL and save the spreadsheet ID. This will be the long string of random letters and numbers. For example, if my spreadsheet URL were `https://docs.google.com/spreadsheets/d/1luDE6PCo2CCBuQAF51bfig9GACMSBQh1c6oX9aw3n64/edit?usp=sharing`, then my spreadsheet ID would be `1luDE6PCo2CCBuQAF51bfig9GACMSBQh1c6oX9aw3n64`. Then, paste this ID as the value for `SPREADSHEET_ID` in the `keys.json` file.

3. **Generate a Google Sheets API key**

Go to the [Credentials page](https://console.developers.google.com/apis/credentials) in the Google Developers API console and generate an API key. Make sure that the project that you generate your API key for has Google Sheets enabled. Once you have your API key, save as the value for `GOOGLE_API_KEY` in `keys.json`.

4. **Write the email that you want to send**

Once you have your keys saved, you'll have to write out the subject line and text to the email that you want to send. Follow the format of the `.email` files that already exist, and place your new file in the `emails` folder. Keep in mind that the line breaks matter, as these determine where your paragraphs will start and end.

5. **Send your email out to everyone**

Finally, once everything is in place, you'll be able to send your email from the command line. Perform the following command...

```bash
$ python send.py filename
```

...where `filename` is the name of the file (before `.email`) that you put in the `emails` folder in the last step. You should now see messages telling you about each email that is getting sent out.

## License

`email` is available under the MIT license. See the LICENSE file for details.
