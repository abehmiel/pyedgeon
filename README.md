# pyedgeon

Create stunning optical illusion images with hidden text that appears when viewed at an angle!

Pyedgeon is a Python library that generates circular images containing text that's hidden when viewed directly but becomes readable when the image is tilted and viewed nearly edge-on. This effect is created using circular anamorphic distortion - a mathematical transformation that compensates for perspective foreshortening.

![alt text](https://abehmiel.files.wordpress.com/2017/01/npr-cool-dad-rock.png?w=610 "See if you can read: 'NPR COOL DAD ROCK'")

The solution to the above illusion is "NPR COOL DAD ROCK" ;)

**Tip**: View generated images on a mobile device or tablet for the best experience - you can easily tilt the device to see the hidden message!

## Quick Start

### Installation

Install via pip:

```bash
pip install pyedgeon
```

### Font Requirements

Pyedgeon requires a TrueType font (.ttf) or TrueType Collection (.ttc) to render text. **The library will automatically search for and use system fonts**, so in most cases you don't need to do anything!

**Supported Platforms**:
- ✅ **macOS**: Automatically finds Helvetica or Helvetica Neue
- ✅ **Linux**: Automatically finds DejaVu Sans or Liberation Sans
- ✅ **Windows**: Automatically finds Arial or Calibri

**If you want to use a specific font**, simply provide the `font_path` parameter:

```python
img = Pyedgeon(
    illusion_text="HELLO",
    font_path="/path/to/your/font.ttf"  # Use your preferred font
)
```

**Finding Fonts on Your System**:
- **macOS**: `/System/Library/Fonts/` or `/Library/Fonts/`
- **Linux**: `/usr/share/fonts/truetype/`
- **Windows**: `C:\Windows\Fonts\`

### **Important Readability Note!**

When testing this package I've found better success with lighter fonts. Personally
I think that pyedgeon buttons look best with the DejaVuSans-ExtraLight.ttf font (not distributed),
but it's easy to find and install this font and specify the path to it in the API.

### Basic Usage

#### Option 1: Quick-Start Script (Easiest!)

The quickest way to create an image is using the included example script:

```bash
# Clone the repository
git clone https://github.com/abehmiel/pyedgeon.git
cd pyedgeon

# Install dependencies
make install

# Create a default "HELLO WORLD" image
make example

# Or customize the message
make example MESSAGE="SECRET TEXT"
```

You can also run the script directly for more options:

```bash
# Basic usage
python scripts/example.py

# Custom message
python scripts/example.py "YOUR MESSAGE"

# Specify custom font
python scripts/example.py "YOUR MESSAGE" --font /path/to/font.ttf

# Custom output filename
python scripts/example.py "YOUR MESSAGE" --output my_image.png

# See all options
python scripts/example.py --help
```

#### Option 2: Using as a Python Library

```python
from pyedgeon import Pyedgeon

# Create an illusion image with default settings
img = Pyedgeon(illusion_text="HELLO WORLD")
img.create()
# Creates: HELLO WORLD.png in current directory
```

That's it! The image will be saved in your current working directory.

## Advanced Usage

### Customization Options

### Full Example

```python
from pyedgeon import Pyedgeon

img = Pyedgeon(
    illusion_text="CUSTOM TEXT",           # Text to display (auto-uppercase by default)
    # font_path="/path/to/font.ttf",       # Optional: custom font (auto-detected if omitted)
    num_rotations=6,                       # Number of text rotations (default: 6)
    img_side=2048,                         # Image size in pixels (default: 1024)
    text_color=(255, 0, 0),                # RGB color for text (default: black)
    background_color=(255, 255, 255),      # RGB color for background (default: white)
    file_path="/output/directory/",        # Output directory (default: current dir)
    file_name="my_illusion",               # Output filename (default: illusion_text)
    file_ext=".png",                       # File format (default: .png)
    charmax=22,                            # Max characters (default: 22)
    upper_case=True                        # Convert to uppercase (default: True)
)
img.create()
```

### Parameter Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `illusion_text` | str | "HELLO WORLD" | Text to display in the illusion |
| `font_path` | str | None | Path to TrueType font file (auto-detected if None) |
| `num_rotations` | int | 6 | Number of text rotations around circle |
| `img_side` | int | 1024 | Size of square image in pixels |
| `text_color` | tuple | (0, 0, 0) | RGB color for text (0-255) |
| `background_color` | tuple | (255, 255, 255) | RGB color for background (0-255) |
| `file_path` | str | "" | Directory path for output (empty = current dir) |
| `file_name` | str | None | Output filename without extension (None = use text) |
| `file_ext` | str | ".png" | File format extension |
| `charmax` | int | 22 | Maximum character limit |
| `crop_width_x` | int | 14 | Horizontal padding for text bounding box |
| `crop_width_y` | int | 5 | Vertical padding for text bounding box |
| `darkness_threshold` | int | 116 | Threshold for black/white conversion (0-255) |
| `upper_case` | bool | True | Automatically convert text to uppercase |

For detailed parameter descriptions, see [API_REFERENCE.md](API_REFERENCE.md). 

## Usage Tips

### Viewing the Illusion

1. **Mobile/Tablet**: Best viewing experience - tilt device to nearly edge-on
2. **Desktop**: Hold screen at eye level and view from an extreme angle
3. **Print**: Works great on physical prints - hold at eye level and tilt

### Best Practices

- **Text Length**: Keep text between 15-22 characters for best results
- **Font Choice**: Extra-light or light weight fonts work best
- **Colors**: High contrast between text and background recommended
- **Image Size**: Use 1024 for web display, 2048+ for printing
- **Rotations**: 6-8 rotations provide good visibility from multiple angles

## Accessing the Image Object

The generated image is available in memory after creation:

```python
img = Pyedgeon(illusion_text="HELLO")
img.create()

# Access the PIL Image object
pil_image = img.full_image

# Perform additional operations
pil_image.show()           # Display in image viewer
pil_image.resize((512, 512))  # Resize
pil_image.save("copy.png")    # Save additional copy
```

## Documentation

Comprehensive documentation is available:

- **[API_REFERENCE.md](API_REFERENCE.md)** - Detailed API documentation with examples
- **[CLAUDE.md](CLAUDE.md)** - Developer documentation, architecture, and algorithms
- **[SECURITY.md](SECURITY.md)** - Security guidelines for safe usage
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guide for contributors
- **[DOCSTRING_EXAMPLES.md](DOCSTRING_EXAMPLES.md)** - Enhanced docstring examples

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Code guidelines
- Testing requirements
- Pull request process
- Priority areas for contribution

## Related Projects

**[pyedgeon-service](https://github.com/abehmiel/pyedgeon-service)** - A web service that uses this API to generate illusions online!

## License

MIT License - see LICENSE file for details

## Author

Abraham Hmiel (abehmiel@gmail.com)

## Acknowledgments

Special thanks to all contributors and users of this library! 
