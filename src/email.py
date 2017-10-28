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
        self.subject = lines[0].split(": ", 1)[1]

        text = ""

        # Start at 2 to remove the subject line and the newline
        # End at -1 to remove the last newline in the file
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

    try:
        f = open("./emails/%s.email" % name)
    except FileNotFoundError:
        print("\"%s\" could not be found. Make sure that %s.email exists in the emails folder." % (name, name))
        return None

    contents = f.read()
    f.close()

    email = Email(contents)
    return email
