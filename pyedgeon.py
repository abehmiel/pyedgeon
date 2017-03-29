from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from math import sqrt
 
# Primary user-editable settings
################################
illusion_text = "NPR COOL DAD ROCK"
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf"
num_rotations = 6
file_ext = ".png"

# Additional settings
################################
text_color = (0, 0, 0)
background_color = (255, 255, 255)
img_side = 1024
charmax = 18
font_size_guess = 7*(30-len(illusion_text))
crop_width_x = 14
crop_width_y = 5
darkness_threshold = 114
 
# Fail if sentence is too long (it looks ugly)
if len(illusion_text) <= charmax:
    pass
else:
    print('WARNING: Text too long. Exiting.')
    raise SystemExit(0)
 
img_size = (img_side, img_side)
img_size_text = (img_side, img_side)
 
raw_img = Image.new("RGB", img_size_text, background_color)
img = Image.new("RGBA", img_size, background_color)
circle_img = Image.new("RGBA", img_size, background_color)
full_image = Image.new("RGBA", img_size, background_color)
draw = ImageDraw.Draw(raw_img)
 
# step through font sizes to find optimal font for box
for font_trial in range(font_size_guess-30, font_size_guess+30):
    possible_font = ImageFont.truetype(font_path, font_trial)
    raw_img = Image.new("RGB", img_size_text, background_color)
    draw = ImageDraw.Draw(raw_img)
    draw.text((crop_width_x, crop_width_y), illusion_text, text_color, font=possible_font)
 
    # find bounding box of text by inversion
    inverted = ImageOps.invert(raw_img)
    possible_boundingbox = (inverted.getbbox()[0] - crop_width_x, \
                            inverted.getbbox()[1] - crop_width_y, \
                            inverted.getbbox()[2] + crop_width_x, \
                            inverted.getbbox()[3] + crop_width_y)
    if possible_boundingbox[2] - possible_boundingbox[0] < img_side-2*crop_width_x:
        boundingbox = possible_boundingbox
        font_size = font_trial
    else:
        break
 
# Start drawing boxes
raw_img = Image.new("RGB", img_size_text, background_color)
draw = ImageDraw.Draw(raw_img)
font = ImageFont.truetype(font_path, font_size)
draw.text((crop_width_x, crop_width_y), illusion_text, text_color, font=font)
inverted = ImageOps.invert(raw_img)
raw_img = raw_img.crop(boundingbox)
scaled_img = raw_img.resize((img_side, img_side), Image.BICUBIC)
img.paste(scaled_img, (0, 0))
 
# map points in the square image to points in a circle
# turn light grey and white to alpha channel. Blacken dark grays.
pixdata = img.load()
for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pixdata[x, y] == (255, 255, 255, 255):
            pixdata[x, y] = (255, 255, 255, 0)
        elif pixdata[x, y][1] >= darkness_threshold:
            pixdata[x, y] = (255, 255, 255, 0)
        elif pixdata[x, y][1] <= darkness_threshold:
            pixdata[x, y] = (0, 0, 0, 255)
 
circle_img.paste(img, (0, 0))
pixdata2 = circle_img.load()

# Stretch text vertically along the path of a circle
for x in range(img_side):
    Ysize = 2 * sqrt((img_side / 2) ** 2 - (x - (img_side / 2)) ** 2)
    for y in range(img_side):
        Yoffset = int((img_side-Ysize)/2.)
        Y = Yoffset + int((Ysize/img_side)*y)
        pixdata2[x, Y] = pixdata[x, y]
        if sqrt((x-img_side/2)**2 + (y-img_side/2)**2) >= img_side/2 - 2:
            pixdata2[x, y] = (255, 255, 255, 0)
 
# Stamp text repeatedly in a circular manner
for i in range(num_rotations):
    this_circle = circle_img.rotate(i*180/num_rotations)
    full_image.paste(this_circle, (0, 0), this_circle)
 
# Turn alpha channel back to white
pixdata = full_image.load()
for y in range(full_image.size[1]):
    for x in range(full_image.size[0]):
        if pixdata[x, y] == (255, 255, 255, 0):
            pixdata[x, y] = (255, 255, 255, 255)
 
# Save as png
full_image.save(illusion_text+file_ext)
