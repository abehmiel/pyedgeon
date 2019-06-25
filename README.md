# pyedgeon
Simple class to generate circular images that read a short phrase when held at eye level, nearly edge-on. PIL is used for image processing.

The code has basic functionality and some user-editable settings like choosing the path to the font file, size of the output image, and what words to write. 

It's a lot easier to view the generated images on a mobile or tablet where you can freely orient the device in space.  After running the script, you should obtain an image like this:

![alt text](https://abehmiel.files.wordpress.com/2017/01/npr-cool-dad-rock.png?w=610 "See if you can read: 'NPR COOL DAD ROCK'")

## Usage

`from pyedgeon import Pyedgeon`

`test = Pyedgeon(illusion_text="hello world")`

`test.create()`

full list of options with defaults:

`test = Pyedgeon(illusion_text="hello world", font_path = "DejaVuSans-ExtraLight.ttf", num_rotations = 6, file_ext = ".png", text_color = (0, 0, 0), background_color = (255, 255, 255), img_side = 1024, charmax = 22, crop_width_x = 14, crop_width_y = 15, darkness_threshold = 116, upper_case = True)`

illusion_text: Text in the button. Will be automatically casted to upper-case by default.

num_rotations: The number of times the text will be stamped around the circle, at intervals of 180/num_rotations degrees.

file_ext: File format for output.

text_color: 3-tuple of values 0:255 for controlling the text color

background_color: 3-tuple of values 0:255 for controlling the background color

img_side: Size of image in pixels, per side.

charmax: Maximum character limit. Works best when around 22 for many fonts, but may need to be changed if you are using uncommon or very narrow fonts.

crop_width_x: Adjusts overlap of bounding box and image on the left and right edges of text.

crop_width_y: Adjusts overlap of bounding box and image on the top and bottom edges of text.

darkness_threshold: Threshold for step function which transforms gray pixels to black or white during image creation.

filepath: (use a forward slash to end the string) a folder location to save the file

upper_case: set to False to use lower-case characters. 

### Outputs

The .create() method will save a file to the current working directory:

- `self.filepath+self.illusion_text+self.file_ext`

Meanwhile, `self.full_image` has the image in memory.
