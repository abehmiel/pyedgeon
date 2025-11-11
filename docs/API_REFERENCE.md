# Pyedgeon API Reference

## Table of Contents

1. [Overview](#overview)
2. [Class: Pyedgeon](#class-pyedgeon)
3. [Constructor Parameters](#constructor-parameters)
4. [Public Methods](#public-methods)
5. [Usage Examples](#usage-examples)
6. [Error Handling](#error-handling)
7. [Type Definitions](#type-definitions)

## Overview

Pyedgeon provides a simple API for generating optical illusion images. The main interface is the `Pyedgeon` class, which encapsulates all configuration and processing.

### Quick Start

```python
from pyedgeon import Pyedgeon

# Basic usage
img = Pyedgeon(illusion_text="HELLO WORLD")
img.create()
```

## Class: Pyedgeon

```python
class Pyedgeon(
    illusion_text="HELLO WORLD",
    font_path="DejaVuSans-ExtraLight.ttf",
    num_rotations=6,
    file_ext=".png",
    text_color=(0, 0, 0),
    background_color=(255, 255, 255),
    img_side=1024,
    charmax=22,
    crop_width_x=14,
    crop_width_y=5,
    darkness_threshold=116,
    file_name=None,
    file_path="",
    upper_case=True
)
```

Main class for creating optical illusion images with circular anamorphic text distortion.

## Constructor Parameters

### illusion_text
- **Type**: `str`
- **Default**: `"HELLO WORLD"`
- **Description**: The text to display in the optical illusion.
- **Constraints**:
  - Maximum length determined by `charmax` parameter
  - Automatically converted to uppercase if `upper_case=True`
  - Text longer than `charmax` will be truncated with a warning
- **Example**:
  ```python
  img = Pyedgeon(illusion_text="NPR COOL DAD ROCK")
  ```

### font_path
- **Type**: `str`
- **Default**: `"DejaVuSans-ExtraLight.ttf"`
- **Description**: Path to TrueType font file (.ttf) to use for rendering text.
- **Constraints**:
  - Must be a valid path to a .ttf font file
  - Font must be accessible by the Python process
  - Recommended: Use extra-light or light weight fonts for best results
- **Security Warning**: Path is not validated - see [Security Considerations](#security-considerations)
- **Example**:
  ```python
  img = Pyedgeon(
      illusion_text="HELLO",
      font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf"
  )
  ```

### num_rotations
- **Type**: `int`
- **Default**: `6`
- **Description**: Number of times the text is stamped around the circle at equal intervals.
- **Valid Range**: 1 to ~12 (higher values may cause text overlap)
- **Notes**:
  - Text is stamped at intervals of `180 / num_rotations` degrees
  - More rotations = text visible from more angles
  - Fewer rotations = clearer text, less overlap
- **Example**:
  ```python
  # Text stamped every 45 degrees (180/4 = 45)
  img = Pyedgeon(illusion_text="HELLO", num_rotations=4)
  ```

### file_ext
- **Type**: `str`
- **Default**: `".png"`
- **Description**: File extension for the output image.
- **Valid Values**: Any format supported by PIL (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, etc.)
- **Notes**:
  - Must include leading dot (`.png` not `png`)
  - PNG recommended for lossless quality
  - JPEG may introduce compression artifacts
- **Example**:
  ```python
  img = Pyedgeon(illusion_text="HELLO", file_ext=".jpg")
  ```

### text_color
- **Type**: `Tuple[int, int, int]`
- **Default**: `(0, 0, 0)` (black)
- **Description**: RGB color tuple for the text.
- **Valid Range**: Each component 0-255
- **Format**: `(red, green, blue)`
- **Example**:
  ```python
  # Red text
  img = Pyedgeon(illusion_text="HELLO", text_color=(255, 0, 0))

  # Dark gray text
  img = Pyedgeon(illusion_text="HELLO", text_color=(64, 64, 64))
  ```

### background_color
- **Type**: `Tuple[int, int, int]`
- **Default**: `(255, 255, 255)` (white)
- **Description**: RGB color tuple for the background.
- **Valid Range**: Each component 0-255
- **Format**: `(red, green, blue)`
- **Notes**: High contrast between text and background recommended for best results
- **Example**:
  ```python
  # White text on black background
  img = Pyedgeon(
      illusion_text="HELLO",
      text_color=(255, 255, 255),
      background_color=(0, 0, 0)
  )
  ```

### img_side
- **Type**: `int`
- **Default**: `1024`
- **Description**: Size of the output image in pixels (width and height - image is always square).
- **Valid Range**: 128 to 4096 (recommended)
- **Notes**:
  - Larger images take longer to process
  - Very large images (>4096) may cause memory issues
  - Recommended: 1024 for web, 2048 for print
- **Performance**: Processing time scales with O(n²)
- **Example**:
  ```python
  # High resolution for print
  img = Pyedgeon(illusion_text="HELLO", img_side=2048)
  ```

### charmax
- **Type**: `int`
- **Default**: `22`
- **Description**: Maximum number of characters allowed in the text.
- **Valid Range**: 1 to ~30 (depends on font and img_side)
- **Notes**:
  - Longer text requires smaller font size
  - Text exceeding this limit will be truncated
  - Optimal value depends on font character width
- **Example**:
  ```python
  # Allow longer text with larger image
  img = Pyedgeon(
      illusion_text="A VERY LONG MESSAGE HERE",
      charmax=30,
      img_side=2048
  )
  ```

### crop_width_x
- **Type**: `int`
- **Default**: `14`
- **Description**: Horizontal padding (in pixels) added to text bounding box on left and right edges.
- **Valid Range**: 0 to 50
- **Purpose**: Provides visual breathing room around text
- **Notes**: Affects font size calculation - larger values result in smaller fonts
- **Example**:
  ```python
  # More horizontal padding
  img = Pyedgeon(illusion_text="HELLO", crop_width_x=20)
  ```

### crop_width_y
- **Type**: `int`
- **Default**: `5`
- **Description**: Vertical padding (in pixels) added to text bounding box on top and bottom edges.
- **Valid Range**: 0 to 50
- **Purpose**: Provides visual breathing room around text
- **Notes**: Lower than crop_width_x because text is horizontally oriented
- **Example**:
  ```python
  # More vertical padding
  img = Pyedgeon(illusion_text="HELLO", crop_width_y=10)
  ```

### darkness_threshold
- **Type**: `int`
- **Default**: `116`
- **Description**: Threshold value for converting grayscale pixels to black or white.
- **Valid Range**: 0 to 255
- **Purpose**: Controls anti-aliasing vs. sharp edges
- **Behavior**:
  - Pixels with green channel value >= threshold → white (background)
  - Pixels with green channel value < threshold → black (text)
- **Notes**:
  - Lower values (e.g., 80) = more anti-aliasing, softer edges
  - Higher values (e.g., 180) = sharper edges, less anti-aliasing
- **Example**:
  ```python
  # Sharper text edges
  img = Pyedgeon(illusion_text="HELLO", darkness_threshold=180)
  ```

### file_name
- **Type**: `str` or `None`
- **Default**: `None` (uses `illusion_text` as filename)
- **Description**: Base filename for the output image (without extension).
- **Notes**:
  - Extension is added automatically from `file_ext`
  - If None, uses `illusion_text` as filename
  - Should not include path separators
- **Security Warning**: Not sanitized - use caution with user input
- **Example**:
  ```python
  img = Pyedgeon(
      illusion_text="HELLO WORLD",
      file_name="my_custom_name"
  )
  # Saves as: my_custom_name.png
  ```

### file_path
- **Type**: `str`
- **Default**: `""` (current working directory)
- **Description**: Directory path where the output image will be saved.
- **Format**: Should end with `/` or be empty string
- **Notes**:
  - Empty string (`""`) = current working directory
  - Can be absolute or relative path
  - Directory must exist (not created automatically)
- **Security Warning**: Path is not validated - see [Security Considerations](#security-considerations)
- **Example**:
  ```python
  # Save to specific directory
  img = Pyedgeon(
      illusion_text="HELLO",
      file_path="/home/user/images/"
  )

  # Save to subdirectory
  img = Pyedgeon(
      illusion_text="HELLO",
      file_path="output/"
  )
  ```

### upper_case
- **Type**: `bool`
- **Default**: `True`
- **Description**: Whether to automatically convert text to uppercase.
- **Notes**:
  - Uppercase text generally works better for optical illusions
  - Set to `False` to preserve mixed or lowercase text
- **Example**:
  ```python
  # Preserve original case
  img = Pyedgeon(
      illusion_text="Hello World",
      upper_case=False
  )
  ```

## Public Methods

### create()

```python
def create() -> None
```

Executes the complete image generation pipeline and saves the result to disk.

**Pipeline Steps**:
1. Validates text length (`check_length`)
2. Estimates appropriate font size (`estimate_font_size`)
3. Creates image canvases (`draw_clear`)
4. Refines font size to fit (`get_fontsize`)
5. Renders and distorts text (`draw_frame`)
6. Stamps multiple rotations (`stamp`)
7. Converts alpha channel to background color (`alpha_to_white`)
8. Saves image to disk (`save_img`)

**Returns**: `None`

**Side Effects**:
- Creates/overwrites file at `file_path/file_name + file_ext`
- Sets internal state attributes (`self.full_image`, `self.font`, etc.)

**Raises**:
- `FileNotFoundError`: If font file doesn't exist
- `PermissionError`: If cannot write to output location
- `OSError`: If output directory doesn't exist

**Example**:
```python
img = Pyedgeon(illusion_text="HELLO WORLD")
img.create()  # Saves "HELLO WORLD.png" in current directory
```

### check_length()

```python
def check_length() -> None
```

Validates that text length does not exceed `charmax`. Truncates and warns if too long.

**Returns**: `None`

**Side Effects**:
- Modifies `self.illusion_text` if text is too long
- Prints warning to stdout if truncating

**Known Issue**: Truncates to 20 characters instead of `self.charmax`

**Example**:
```python
img = Pyedgeon(illusion_text="A" * 30, charmax=10)
img.check_length()
# Prints: WARNING: Text too long. Truncating
# Sets: img.illusion_text = "A" * 20
```

### estimate_font_size()

```python
def estimate_font_size() -> None
```

Estimates appropriate font size using character width heuristics.

**Returns**: `None`

**Side Effects**: Sets `self.font_size_guess` attribute

**Algorithm**:
- Assigns width values to each character based on visual width
- Sums total width
- Applies empirical formula: `font_size = min(max(int(280 - 18.7*width), 60), 220)`

**Example**:
```python
img = Pyedgeon(illusion_text="HELLO")
img.estimate_font_size()
print(img.font_size_guess)  # e.g., 178
```

### draw_clear()

```python
def draw_clear() -> None
```

Initializes blank image canvases for the rendering pipeline.

**Returns**: `None`

**Side Effects**: Creates attributes:
- `self.raw_img`: RGB canvas for text rendering
- `self.img`: RGBA canvas for transformation
- `self.circle_img`: RGBA canvas for circular distortion
- `self.full_image`: RGBA canvas for final composite
- `self.draw`: ImageDraw object for raw_img

**Example**:
```python
img = Pyedgeon(illusion_text="HELLO")
img.draw_clear()
# Creates blank canvases
```

### get_fontsize()

```python
def get_fontsize() -> Tuple[int, Tuple[int, int, int, int]]
```

Refines font size estimate to find largest font that fits within image bounds.

**Returns**: Tuple of `(font_size, bounding_box)`
- `font_size`: Integer font size in points
- `bounding_box`: Tuple of `(left, top, right, bottom)` pixel coordinates

**Side Effects**:
- Sets `self.font_size`, `self.font`, and `self.boundingbox` attributes
- Creates 60+ temporary images during search
- May recurse if no suitable size found

**Performance**: O(n) linear search creating n temporary images

**Known Issues**:
- Bare except clause hides errors
- Unbounded recursion can cause stack overflow

**Example**:
```python
img = Pyedgeon(illusion_text="HELLO")
img.estimate_font_size()
img.draw_clear()
font_size, bbox = img.get_fontsize()
print(f"Font size: {font_size}, Bounding box: {bbox}")
```

### draw_frame()

```python
def draw_frame() -> None
```

Renders text and applies circular anamorphic distortion.

**Returns**: `None`

**Side Effects**:
- Modifies `self.img` and `self.circle_img` with transformed pixels
- Creates `self.raw_img` and `self.scaled_img`

**Algorithm**:
1. Render text to canvas
2. Crop to bounding box
3. Scale to target size
4. Apply darkness threshold (convert to black/white with alpha)
5. Apply circular distortion transformation

**Performance**: O(n²) pixel iteration

**Example**:
```python
img = Pyedgeon(illusion_text="HELLO")
img.estimate_font_size()
img.draw_clear()
img.get_fontsize()
img.draw_frame()
# self.circle_img now contains distorted text
```

### stamp()

```python
def stamp() -> None
```

Rotates and composites the circular image multiple times.

**Returns**: `None`

**Side Effects**: Updates `self.full_image` with composited rotations

**Algorithm**:
- For each rotation (0 to num_rotations-1):
  - Rotate circle_img by `i * 180 / num_rotations` degrees
  - Alpha composite onto full_image

**Example**:
```python
img = Pyedgeon(illusion_text="HELLO", num_rotations=6)
# ... previous steps ...
img.stamp()
# self.full_image now has text stamped 6 times
```

### alpha_to_white()

```python
def alpha_to_white() -> None
```

Converts transparent pixels (alpha=0) back to background color.

**Returns**: `None`

**Side Effects**: Modifies `self.full_image` pixel data

**Known Issue**: Critical syntax error on line 215 (missing `+` operator)

**Purpose**: Remove alpha channel for formats that don't support transparency

**Example**:
```python
img = Pyedgeon(illusion_text="HELLO")
# ... previous steps ...
img.alpha_to_white()
# Transparent pixels now white (or background_color)
```

### save_img()

```python
def save_img() -> None
```

Saves the final image to disk.

**Returns**: `None`

**Side Effects**: Creates/overwrites file on disk

**File Location**: `file_path/file_name + file_ext`

**Raises**:
- `PermissionError`: If cannot write to location
- `OSError`: If directory doesn't exist

**Example**:
```python
img = Pyedgeon(
    illusion_text="HELLO",
    file_path="/home/user/",
    file_name="test",
    file_ext=".png"
)
# ... previous steps ...
img.save_img()
# Saves to: /home/user/test.png
```

### get_file_path()

```python
def get_file_path() -> str
```

Constructs the full file path for the output image.

**Returns**: String representation of the file path

**Behavior**:
- If `file_path == ""`: Uses current working directory
- Otherwise: Uses specified path
- Combines path, filename, and extension

**Example**:
```python
img = Pyedgeon(
    illusion_text="HELLO",
    file_path="/output/",
    file_name="test",
    file_ext=".png"
)
path = img.get_file_path()
# Returns: "/output/test.png"
```

## Usage Examples

### Example 1: Basic Usage

```python
from pyedgeon import Pyedgeon

# Create image with default settings
img = Pyedgeon(illusion_text="HELLO WORLD")
img.create()
# Output: HELLO WORLD.png in current directory
```

### Example 2: Custom Colors and Size

```python
from pyedgeon import Pyedgeon

# White text on black background, high resolution
img = Pyedgeon(
    illusion_text="OPTICAL ILLUSION",
    text_color=(255, 255, 255),      # White
    background_color=(0, 0, 0),      # Black
    img_side=2048,                   # High res
    file_name="illusion_highres"
)
img.create()
# Output: illusion_highres.png (2048x2048, white on black)
```

### Example 3: Custom Font and Path

```python
from pyedgeon import Pyedgeon

# Use custom font and save to specific location
img = Pyedgeon(
    illusion_text="CUSTOM FONT",
    font_path="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    file_path="/home/user/output/",
    file_name="custom",
    file_ext=".jpg"
)
img.create()
# Output: /home/user/output/custom.jpg
```

### Example 4: More Rotations

```python
from pyedgeon import Pyedgeon

# Increase number of text rotations
img = Pyedgeon(
    illusion_text="MORE ANGLES",
    num_rotations=12,  # Text every 15 degrees (180/12)
    file_name="many_rotations"
)
img.create()
# Output: many_rotations.png with text stamped 12 times
```

### Example 5: Accessing Image Object

```python
from pyedgeon import Pyedgeon
from PIL import Image

# Generate image and access PIL Image object
img = Pyedgeon(illusion_text="IMAGE OBJECT")
img.create()

# Access the PIL Image object
pil_image = img.full_image

# Perform additional operations
pil_image = pil_image.resize((512, 512))
pil_image.show()  # Display in viewer
pil_image.save("modified.png")
```

### Example 6: Batch Generation

```python
from pyedgeon import Pyedgeon

phrases = ["PHRASE ONE", "PHRASE TWO", "PHRASE THREE"]

for phrase in phrases:
    img = Pyedgeon(
        illusion_text=phrase,
        file_name=phrase.replace(" ", "_").lower(),
        file_path="batch_output/"
    )
    img.create()
    print(f"Created {phrase}")

# Output:
# batch_output/phrase_one.png
# batch_output/phrase_two.png
# batch_output/phrase_three.png
```

### Example 7: Fine-Tuning Parameters

```python
from pyedgeon import Pyedgeon

# Fine-tune for specific font characteristics
img = Pyedgeon(
    illusion_text="NARROW FONT",
    font_path="NarrowFont.ttf",
    charmax=30,           # Allow more characters for narrow font
    crop_width_x=20,      # More horizontal padding
    crop_width_y=10,      # More vertical padding
    darkness_threshold=140  # Sharper edges
)
img.create()
```

## Error Handling

### Common Errors and Solutions

#### FileNotFoundError: Font Not Found

```python
try:
    img = Pyedgeon(
        illusion_text="HELLO",
        font_path="nonexistent.ttf"
    )
    img.create()
except FileNotFoundError as e:
    print(f"Font file not found: {e}")
    # Solution: Verify font path or use default
    img = Pyedgeon(illusion_text="HELLO")  # Use default font
    img.create()
```

#### PermissionError: Cannot Write File

```python
try:
    img = Pyedgeon(
        illusion_text="HELLO",
        file_path="/root/protected/"  # No write permission
    )
    img.create()
except PermissionError as e:
    print(f"Cannot write to directory: {e}")
    # Solution: Use writable directory
    img.file_path = "/tmp/"
    img.create()
```

#### Text Too Long Warning

```python
img = Pyedgeon(
    illusion_text="THIS IS A VERY LONG TEXT THAT EXCEEDS THE MAXIMUM",
    charmax=20
)
img.create()
# Prints: WARNING: Text too long. Truncating
# Text is truncated automatically
```

### Recommended Error Handling Pattern

```python
from pyedgeon import Pyedgeon
from pathlib import Path
import sys

def safe_create_illusion(text, output_path):
    """Safely create illusion image with error handling"""
    try:
        # Validate output directory exists
        output_dir = Path(output_path).parent
        if not output_dir.exists():
            raise ValueError(f"Output directory does not exist: {output_dir}")

        # Create image
        img = Pyedgeon(
            illusion_text=text[:22],  # Enforce character limit
            file_path=str(output_dir) + "/",
            file_name=Path(output_path).stem
        )
        img.create()

        print(f"Successfully created: {output_path}")
        return True

    except FileNotFoundError as e:
        print(f"Error: Font file not found - {e}", file=sys.stderr)
        return False
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: Unexpected error - {e}", file=sys.stderr)
        return False

# Usage
success = safe_create_illusion("HELLO WORLD", "/output/test.png")
```

## Security Considerations

### Path Traversal Vulnerability

The current implementation does not validate file paths, allowing potential path traversal attacks.

**Vulnerable Code**:
```python
# UNSAFE - accepts arbitrary paths
user_input = "../../../../etc/passwd"
img = Pyedgeon(
    illusion_text="HELLO",
    file_path=user_input  # Can write anywhere!
)
```

**Safe Alternative**:
```python
from pathlib import Path

def safe_path(user_path, allowed_base="/safe/output/"):
    """Validate path is within allowed directory"""
    base = Path(allowed_base).resolve()
    target = (base / user_path).resolve()

    # Ensure target is within base directory
    if not str(target).startswith(str(base)):
        raise ValueError("Path traversal detected")

    return str(target)

# Usage
safe_output = safe_path(user_input)
img = Pyedgeon(
    illusion_text="HELLO",
    file_path=safe_output + "/"
)
```

### Input Validation

Always validate user inputs before passing to Pyedgeon:

```python
def validate_inputs(text, img_size, num_rot):
    """Validate user inputs"""
    # Text length
    if not text or len(text) > 30:
        raise ValueError("Text must be 1-30 characters")

    # Image size
    if not (128 <= img_size <= 4096):
        raise ValueError("Image size must be 128-4096")

    # Number of rotations
    if not (1 <= num_rot <= 20):
        raise ValueError("Number of rotations must be 1-20")

    return True

# Usage
try:
    validate_inputs(user_text, user_size, user_rotations)
    img = Pyedgeon(
        illusion_text=user_text,
        img_side=user_size,
        num_rotations=user_rotations
    )
    img.create()
except ValueError as e:
    print(f"Invalid input: {e}")
```

### Resource Limits

Prevent resource exhaustion:

```python
MAX_IMAGE_SIZE = 4096
MAX_TEXT_LENGTH = 30

img = Pyedgeon(
    illusion_text=user_text[:MAX_TEXT_LENGTH],
    img_side=min(user_size, MAX_IMAGE_SIZE)
)
```

## Type Definitions

For developers using type hints, here are the recommended type definitions:

```python
from typing import Tuple, Optional

RGB = Tuple[int, int, int]
RGBA = Tuple[int, int, int, int]
BoundingBox = Tuple[int, int, int, int]  # (left, top, right, bottom)

class Pyedgeon:
    illusion_text: str
    font_path: str
    num_rotations: int
    file_ext: str
    text_color: RGB
    background_color: RGB
    img_side: int
    charmax: int
    crop_width_x: int
    crop_width_y: int
    darkness_threshold: int
    file_name: Optional[str]
    file_path: str
    upper_case: bool

    # Internal state
    font_size_guess: Optional[int]
    font_size: Optional[int]
    boundingbox: Optional[BoundingBox]
    full_image: Optional[Image.Image]
```

---

**API Version**: 0.3.1
**Last Updated**: 2025-11-10
**License**: MIT
