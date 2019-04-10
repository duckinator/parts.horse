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

        if page['style'] == 'DIP' or page['style'] == 'PDIP':
            self.draw_dip(canvas, image, page)
        else:
            canvas.text((10, 10),
                'No renderer for {}'.format(page['style']),
                font=self.font,
                fill='black')

        contents = None
        image = image.crop(image.getbbox())
        with io.BytesIO() as output:
            image.save(output, format='PNG')
            contents = output.getvalue()

        return contents

    def draw_dip(self, canvas, image, page):
        pin_count = page['number_of_pins']
        pins = page['pins']
        pins_per_side = len(pins)
        left_offset = max(map(lambda row: len(str(row[0][1])), pins)) * 15
        pin_offset = 20 # pixels
        rect_height = (pins_per_side + 1) * pin_offset
        rect_width = 100

        canvas.rectangle([(left_offset, 0), (left_offset + rect_width, rect_height)],
            fill=None,
            outline='black',
            width=4)

        for idx in range(0, pins_per_side):
            top = (idx + 1) * pin_offset
            text_top = top - 5
            # Left pin line.
            canvas.line([(left_offset - 10, top), (left_offset, top)],
                fill='black',
                width=5)
            # Left pin name.
            canvas.text((0, text_top),
                str(pins[idx][0][1]), font=self.font, fill='black')
            # Left pin number.
            canvas.text((left_offset + 8, text_top),
                str(pins[idx][0][0]), font=self.font, fill='black')

            # Right pin line.
            canvas.line([(left_offset + rect_width, top), (left_offset + rect_width + 10, top)],
                fill='black',
                width=5)
            # Right pin name.
            canvas.text((left_offset + rect_width + 15, text_top),
                pins[idx][1][1], font=self.font, fill='black')
            # Right pin number.
            canvas.text((left_offset + rect_width - 25, text_top),
                pins[idx][1][0], font=self.font, fill='black')
