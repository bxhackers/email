class Email:
    """A model representing an email.

    Attributes:
        subject: The subject line of the email.
        text: The plain text of the email. Currently, the only allowed HTML
            element in here is <br>.
    """

    def __init__(self, contents):
        """Creates an email from the contents of a .email file.

        Args:
            contents: The contents of the .email file.
        """

        lines = contents.split("\n")
        self.subject = lines[0].split(": ")[1]

        text = ""

        for line in lines[2:-1]:
            text += "%s\n" % line

        self.text = text

def load_email(name):
    """Loads an email from a .email file.

    Args:
        name: The name of the file (without the .email extension).

    Returns:
        The email model that was generated from this file.
    """

    f = open("./emails/%s.email" % name)
    contents = f.read()
    f.close()

    email = Email(contents)
    return email
