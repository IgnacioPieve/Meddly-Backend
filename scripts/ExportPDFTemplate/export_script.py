import pdfkit
import jinja2

template_loader = jinja2.FileSystemLoader(searchpath=".")
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template("index.html")

n = .25

data = {
    "name": "Ignacio Pieve Roiger",
    "weight": 72,
    "height": 171,
    'ihc': (n * .75) + .01
}
output_string = template.render(**data)

config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
pdfkit.from_string(output_string, 'output.pdf', css='styles.css', configuration=config)
