import re

from pynliner import Pynliner

def contains_variables(email):
    """Checks if an email contains any member variables.

    Args:
        email: The email to check.

    Returns:
        True if the email contains any member variables.
    """

    return "{{first}}" in email.text or "{{last}}" in email.text or "{{email}}" in email.text

def render_template(email, member=None):
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

    if member is not None:
        # Replace variables with personalized values for each member
        text = text.replace("{{first}}", member.first).replace("{{last}}", member.last).replace("{{email}}", member.email)

    html = html.replace("{{content}}", text)

    f = open("./template/template.css", "r")
    css = f.read()
    f.close()

    return Pynliner().from_string(html).with_cssString(css).run()

def render_template_text(email, member = None):
    """Renders an email in plaintext for a club member, using the contents of
    the email.

    Args:
        email: The model of the email that is being sent.
        member: The member that this email should be sent to.

    Returns:
        The ready-to-send plaintext email that was generated.
    """

    text = email.text

    # Add extra newlines in plaintext emails
    text = text.replace("\n", "\n\n")

    # Replace anchor tags with plaintext links
    for anchor in re.finditer("<a href=\"([^\"]+)\">([^<]+)<\/a>", text):
        url = anchor.group(1)
        content = anchor.group(2)
        text = text.replace("<a href=\"%s\">%s</a>" % (url, content), "%s (%s)" % (content, url))

    if member is not None:
        # Replace variables with personalized values for each member
        text = text.replace("{{first}}", member.first).replace("{{last}}", member.last).replace("{{email}}", member.email)

    if "<br>" in text or "<br/>" in text or "<br />" in text:
        # Replace HTML newlines with plaintext newlines
        text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")

    return text
