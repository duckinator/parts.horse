from pathlib import Path
import sys
sys.path.append(str(Path(__file__, '..', '..').resolve()))

# pylint: disable=wrong-import-position
from jinja2 import Environment, FileSystemLoader
from lib.model.part import Part
from lib.image import ImageGen
# pylint: enable=wrong-import-position


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


def write_html_files():
    phr = PHRender()

    pages = [
        ('home.html', '/index.html', None),
        ('api.html', '/api/index.html', None),
        ('directory.html', '/parts/index.html', {'parts': Part.all()}),
    ]

    for (template, path, page) in pages:
        phr.render(template, path, page)

    for part_name in Part.names():
        page = Part.get_dict(part_name)
        path = page['url_path'] + '/index.html'
        phr.render('directoryentry.html', path, page)


def write_json_files():
    for part_name in Part.names():
        Path(f'_site/parts/{part_name}.json').write_text(
            Path(f'parts/{part_name}.json').read_text()
        )


def write_image_files():
    img = ImageGen()

    imgdir = Path('_site/images/')
    imgdir.mkdir(exist_ok=True)
    for part_name in Part.names():
        img.save(part_name, imgdir / (part_name + '.png'))
        Path(f'_site/parts/{part_name}.json').write_text(
            Path(f'parts/{part_name}.json').read_text()
        )


def write_caddy_file():
    caddyfile_in = Path(__file__, '..', '..', 'config', 'Caddyfile.in').resolve()
    caddyfile_in_contents = caddyfile_in.read_text()
    caddyfile = caddyfile_in.with_suffix('')

    redirects = []
    for part_name in Part.names():
        page = Part.get_dict(part_name)
        destination = page['datasheet_redirect_target']
        for ds in ['datasheets', 'ds']:
            redirects.append(f'redir /{ds}/{part_name} {destination} 302')

    caddyfile_contents = caddyfile_in_contents.format(redirects="\n  ".join(redirects))
    caddyfile.write_text(caddyfile_contents)
    print(f"Wrote {len(caddyfile_contents)} bytes to {caddyfile}.")


if __name__ == "__main__":
    copy_css()
    # /index.html, /api/index.html, /parts/index.html, /parts/<part>/index.html
    write_html_files()
    # /parts/*.json
    write_json_files()
    # /images/<part>png
    write_image_files()
    # config/Caddyfile, /datasheets/*, /ds/*
    write_caddy_file()
