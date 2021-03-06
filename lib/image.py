from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from lib.model.part import Part

class ImageGen:
    font_path = Path(Path.cwd(), 'public', 'fonts', 'Hack-Regular.ttf').resolve()
    font = ImageFont.truetype(str(font_path), 15)
    dimensions = (400, 450)

    def save(self, part_name, filename):
        page = Part.get_dict(part_name)

        image = Image.new('RGBA', self.dimensions, 'black')

        ImageDraw.floodfill(image, (0, 0), (0, 0, 0, 0))
        canvas = ImageDraw.Draw(image)

        if int(page['number_of_pins']) <= 0:
            canvas.text((0, 0),
                        'No pin information.',
                        font=self.font,
                        fill='black')
        if page['style'] == 'DIP' or page['style'] == 'PDIP':
            self.draw_dip(canvas, image, page)
        else:
            canvas.text((10, 10),
                        'No renderer for {}.'.format(page['style']),
                        font=self.font,
                        fill='black')

        image = image.crop(image.getbbox())

        with open(filename, 'wb') as f:
            image.save(f, format='PNG')

        length = len(Path(filename).read_bytes())
        print(f"Wrote {length} bytes to {filename}.")

    def draw_dip(self, canvas, _image, page):
        pin_count = page['number_of_pins']
        pins = page['pins']
        pins_per_side = pin_count // 2

        if pin_count <= 0 or len(pins) == 0:
            left_offset = 30
        else:
            left_offset = max(map(lambda row: len(str(row[0][1])), pins)) * 15
        pin_offset = 20 # pixels
        rect_height = (pins_per_side + 1) * pin_offset
        rect_width = 100

        if len(pins) <= 0:
            left_offset += 20
            canvas.text((0, rect_height + 10),
                        'Pin data is incomplete.',
                        fill='black',
                        font=self.font)

        canvas.rectangle(
            [(left_offset, 0), (left_offset + rect_width, rect_height)],
            fill=None,
            outline='black',
            width=4)

        for idx in range(0, pins_per_side):
            top = (idx + 1) * pin_offset
            text_top = top - 7
            # Left pin line.
            canvas.line([(left_offset - 10, top), (left_offset, top)],
                        fill='black',
                        width=5)
            # Right pin line.
            canvas.line([(left_offset + rect_width, top), (left_offset + rect_width + 10, top)],
                        fill='black',
                        width=5)

            if len(pins) <= 0:
                continue

            # Left pin name.
            canvas.text((0, text_top),
                        pins[idx][0][1],
                        fill='black',
                        font=self.font)
            # Left pin number.
            canvas.text((left_offset + 8, text_top),
                        pins[idx][0][0],
                        fill='black',
                        font=self.font)

            # Right pin name.
            canvas.text((left_offset + rect_width + 15, text_top),
                        pins[idx][1][1],
                        fill='black',
                        font=self.font)
            # Right pin number.
            canvas.text((left_offset + rect_width - 25, text_top),
                        pins[idx][1][0],
                        fill='black',
                        font=self.font)
