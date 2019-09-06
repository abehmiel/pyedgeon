from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from math import sqrt
from string import digits
from pathlib import Path

class Pyedgeon():

    """
    Creates a pyedgeon object
    """

    def __init__(self,
                 illusion_text = "HELLO WORLD",
                 font_path = "DejaVuSans-ExtraLight.ttf",
                 num_rotations = 6,
                 file_ext = ".png",
                 text_color = (0, 0, 0),
                 background_color = (255, 255, 255),
                 img_side = 1024,
                 charmax = 22,
                 crop_width_x = 14,
                 crop_width_y = 5,
                 darkness_threshold = 116,
                 file_name = None,
                 file_path = "",
                 upper_case = True
                 ):

        """
        Default user-editable settings
        """

        if upper_case:
            self.illusion_text = illusion_text.upper()
        else:
            self.illusion_text = illusion_text
        self.font_path = font_path
        self.num_rotations = num_rotations
        self.file_ext = file_ext
        self.text_color = text_color
        self.background_color = background_color
        self.img_side = img_side
        self.charmax = charmax
        self.file_path = file_path
        self.font_size_guess = None
        self.crop_width_x = crop_width_x
        self.crop_width_y = crop_width_y
        self.darkness_threshold = darkness_threshold
        self.img_size = (self.img_side, self.img_side)
        self.img_size_text = (self.img_side, self.img_side)
        if file_name is not None:
            self.file_name = file_name
        else:
            self.file_name = illusion_text
        self.font_size = None


    def check_length(self):
        """
        Fail if sentence is too long (it looks ugly)
        """
        if len(self.illusion_text) <= self.charmax:
            pass
        else:
            print('WARNING: Text too long. Truncating')
            self.illusion_text = self.illusion_text[0:20]


    def draw_clear(self):

        """Create raw image"""

        self.raw_img = Image.new("RGB",
                                 self.img_size_text,
                                 self.background_color)
        self.img = Image.new("RGBA",
                             self.img_size,
                             self.background_color)
        self.circle_img = Image.new("RGBA",
                                    self.img_size,
                                    self.background_color)
        self.full_image = Image.new("RGBA",
                                    self.img_size,
                                    self.background_color)
        self.draw = ImageDraw.Draw(self.raw_img)

    def estimate_font_size(self):
        """
        Rule-based method for arriving at an 'ok' guess for the font size
        """

        size = 0 # in milinches
        for s in self.illusion_text:
            if s in 'lij|\' ': size += 37
            elif s in '![]fI.,:;/\\t': size += 50
            elif s in '`-(){}r"': size += 60
            elif s in '*^zcsJkvxy': size += 85
            elif s in 'aebdhnopqug#$L+<>=?_~FZT' + digits: size += 95
            elif s in 'BSPEAKVXY&UwNRCHD': size += 112
            elif s in 'QGOMm%W@': size += 135
            else: size += 50
        milinches = size * 6 / 1000.0
        self.font_size_guess = int(280 - 18.7*milinches)

    def get_fontsize(self):

        """step through font sizes to find optimal font for box"""

        for font_trial in range(self.font_size_guess-30,
                                self.font_size_guess+30):
            possible_font = ImageFont.truetype(self.font_path,
                                               font_trial)
            raw_img = Image.new("RGB", self.img_size_text,
                                self.background_color)
            draw = ImageDraw.Draw(raw_img)
            draw.text((self.crop_width_x, self.crop_width_y),
                      self.illusion_text,
                      self.text_color,
                      font=possible_font)

            # find bounding box of text by inversion
            inverted = ImageOps.invert(raw_img)
            possible_boundingbox = (inverted.getbbox()[0] - self.crop_width_x,
                                    inverted.getbbox()[1] - self.crop_width_y,
                                    inverted.getbbox()[2] + self.crop_width_x,
                                    inverted.getbbox()[3] + self.crop_width_y)
            if possible_boundingbox[2] - possible_boundingbox[0] < \
                    self.img_side-2*self.crop_width_x:
                boundingbox = possible_boundingbox
                font_size = font_trial
            else:
                self.font_size = font_size
                self.font = ImageFont.truetype(self.font_path, self.font_size)
                self.boundingbox = boundingbox
                return font_size, boundingbox

    def draw_frame(self):

        # Start drawing boxes
        self.raw_img = Image.new("RGB",
                                 self.img_size_text,
                                 self.background_color)
        draw = ImageDraw.Draw(self.raw_img)
        draw.text((self.crop_width_x, self.crop_width_y),
                  self.illusion_text,
                  self.text_color,
                  font=self.font)
        inverted = ImageOps.invert(self.raw_img)
        self.raw_img = self.raw_img.crop(self.boundingbox)
        self.scaled_img = self.raw_img.resize((self.img_side, self.img_side),
                                              Image.BICUBIC)
        self.img.paste(self.scaled_img, (0, 0))

        # map points in the square image to points in a circle
        # turn light grey and white to alpha channel. Blacken dark grays.
        pixdata = self.img.load()
        for y in range(self.img.size[1]):
            for x in range(self.img.size[0]):
                if pixdata[x, y] == self.background_color + (255,):
                    pixdata[x, y] = self.background_color + (0,)
                elif pixdata[x, y][1] >= self.darkness_threshold:
                    pixdata[x, y] = self.background_color + (0,)
                elif pixdata[x, y][1] <= self.darkness_threshold:
                    pixdata[x, y] = self.text_color + (255,)

        self.circle_img.paste(self.img, (0, 0))
        pixdata2 = self.circle_img.load()

        # Stretch text vertically along the path of a circle
        for x in range(self.img_side):
            Ysize = 2 * sqrt((self.img_side / 2) ** 2 - \
                             (x - (self.img_side / 2)) ** 2)
            for y in range(self.img_side):
                Yoffset = int((self.img_side-Ysize)/2.)
                Y = Yoffset + int((Ysize/self.img_side)*y)
                pixdata2[x, Y] = pixdata[x, y]
                if sqrt((x-self.img_side/2)**2 + (y-self.img_side/2)**2) >= \
                        self.img_side/2 - 2:
                    pixdata2[x, y] = self.background_color + (0,)


    def stamp(self):
        """ Stamp text repeatedly in a circular manner """
        for i in range(self.num_rotations):
            this_circle = self.circle_img.rotate(i*180/self.num_rotations)
            self.full_image.paste(this_circle, (0, 0), this_circle)


    def alpha_to_white(self):
        """Turn alpha channel back to white"""
        pixdata = self.full_image.load()
        for y in range(self.full_image.size[1]):
            for x in range(self.full_image.size[0]):
                if pixdata[x, y] == self.background_color + (0,):
                    pixdata[x, y] = self.background_color (255, )

    def save_img(self):
        """ Save as png """
        self.full_image.save(self.get_file_path())

    def get_file_path(self):
        """ return relative file location """
        if self.file_path == '':
            p = Path.cwd()
        else:
            p = Path(self.file_path)

        writefile = self.file_name + self.file_ext
        handle = p / writefile
        # workaround for https://github.com/python-pillow/Pillow/issues/1747
        return str(handle)

    def create(self):
        """ Perform all steps except initialization """
        self.check_length()
        self.estimate_font_size()
        self.draw_clear()
        self.get_fontsize()
        self.draw_frame()
        self.stamp()
        self.alpha_to_white()
        self.save_img()

def demo():
    foo = Pyedgeon()
    foo.check_length()
    foo.estimate_font_size()
    foo.draw_clear()
    foo.get_fontsize()
    foo.draw_frame()
    foo.stamp()
    foo.alpha_to_white()
    foo.save_img()

if __name__ == "__main__":
    demo()

