from lib.model.part import Part
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PHRender:
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

    def get_class_template(self, klass):
        classname = klass.__name__.lower()
        return self.env.get_template(classname + '.html')

    def render(self, template_name, path, page):
        site = Path(__file__, '..', '..', '_site')
        site.resolve().mkdir(exist_ok=True)

        if path[0] == '/':
            path = path[1:]

        destination = site / path
        destination = destination.resolve()

        destination.parent.mkdir(exist_ok=True)
        template = self.env.get_template(template_name)
        contents = template.render(page=page)
        destination.write_text(contents)
        print(f"Wrote {len(contents)} bytes to {destination}.")


def copy_css():
    css_src = Path(__file__, '..', '..', 'public', 'css', 'application.css')
    css_src = css_src.resolve()

    css_contents = css_src.read_text()

    site = Path(__file__, '..', '..', '_site').resolve()
    site.mkdir(exist_ok=True)

    css = site / 'css'

    css.mkdir(exist_ok=True)
    css_dest = css / 'application.css'
    css_dest.write_text(css_contents)

    print(f"Wrote {len(css_contents)} bytes to {css_dest}.")


if __name__ == "__main__":
    phr = PHRender()

    copy_css()

    pages = [
        ('home.html', '/index.html', None),
        ('api.html', '/api/index.html', None),
        ('directory.html', '/parts/index.html', {'parts': Part.all()}),
    ]

    for (template, path, page) in pages:
        phr.render(template, path, page)
