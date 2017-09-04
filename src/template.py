from pynliner import Pynliner

def render_template(email, member):
    f = open("./template/template.html", "r")
    html = f.read()
    f.close()

    text = ""

    for line in email.text.split("\n"):
        text += "<p>%s</p>" % line

    html = html.replace("{{name}}", member.first).replace("{{content}}", text)

    f = open("./template/template.css", "r")
    css = f.read()
    f.close()

    p = Pynliner().from_string(html).with_cssString(css)
    return p.run()
