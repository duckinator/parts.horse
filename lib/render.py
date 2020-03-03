from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class PHRender:
    def __init__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        env.filters['ljust'] = lambda value, *args: value.ljust(*args)
        env.filters['rjust'] = lambda value, *args: value.rjust(*args)
        self.env = env

    def get_class_template(self, class_or_classname):
        if class_or_classname is str:
            classname = class_or_classname
        else:
            classname = class_or_classname.__name__.lower()

        return self.env.get_template(classname + '.html')

    def render(self, classname, page=None):
        web = Path(__file__, '..', 'web')

        if classname == 'home':
            destination = web / 'index.html'
        else:
            destination = web / classname / 'index.html'

        destination = destination.resolve()

        destination.parent.mkdir(exist_ok=True)
        contents = self.get_class_template(classname).render(page)
        destination.write_text(contents)
        print(f"Wrote {len(contents)} bytes to {destination}.")


if __name__ == "__main__":
    phr = PHRender()
    for name in ['home', 'api']:
        phr.render(name)
