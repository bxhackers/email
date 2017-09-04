class Email:
    subject = ""
    text = ""

    def __init__(self, contents):
        lines = contents.split("\n")
        self.subject = lines[0].split(": ")[1]

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
