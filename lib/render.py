from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PHRender:
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

    def get_class_template(self, klass):
        return self.env.get_template(klass.__name__.lower() + '.html')

    def render(self, klass, page=None):
        web = Path(__file__, '..', 'web')
        destination = (web / klass.__name__.lower() / 'index.html').resolve()

        destination.parent.mkdir(exist_ok=True)
        contents = self.get_class_template(klass).render(page)
        destination.write_text(contents)
        print(f"Wrote {len(contents)} bytes to {destination}.")
