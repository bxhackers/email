from pynliner import Pynliner

def render_template(email, member):
    """Renders an email for a club member, using the html/css files from the
    template folder.

    Args:
        email: The model of the email that is being sent.
        member: The member that this email should be sent to.

    Returns:
        The ready-to-send HTML generated from this template, email, and member.
    """

    f = open("./template/template.html", "r")
    html = f.read()
    f.close()

    text = ""

    for line in email.text.split("\n"):
        text += "<p>%s</p>" % line

    # Replace variables with personalized values for each member
    text = text.replace("{{first}}", member.first).replace("{{last}}", member.last).replace("{{email}}", member.email)
    html = html.replace("{{content}}", text)

    f = open("./template/template.css", "r")
    css = f.read()
    f.close()

    p = Pynliner().from_string(html).with_cssString(css)
    return p.run()
