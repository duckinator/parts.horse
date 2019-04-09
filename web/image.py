import cherrypy
import io
from lib.model.part import Part
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class ImageGen(object):
    font_path = Path(Path.cwd(), 'public', 'fonts', 'Awoof-Mono-Regular.ttf').resolve()
    font = ImageFont.truetype(str(font_path), 20)
    dimensions = (400, 400)

    @cherrypy.expose
    @cherrypy.tools.response_env()
    def index(self, part):
        cherrypy.response.headers['Content-Type'] = 'image/png'

        page = Part.get_dict(part)

        image = Image.new('RGBA', self.dimensions, 'black')

        ImageDraw.floodfill(image, (0, 0), (0, 0, 0, 0))
        canvas = ImageDraw.Draw(image)
        canvas.text((10, 10), 'Hello from Pillow!', font=self.font, fill='black')

        contents = None
        with io.BytesIO() as output:
            image.save(output, format='PNG')
            contents = output.getvalue()

        return contents

