"""
Unit tests for Pyedgeon initialization and parameter validation.

Tests cover:
- Constructor parameter handling
- Default value assignments
- Parameter validation
- Type checking
- Boundary conditions
"""

import pytest
from pyedgeon import Pyedgeon


class TestConstructorDefaults:
    """Test that constructor sets appropriate default values."""

    def test_default_illusion_text(self, font_path, temp_dir):
        """Test default illusion text is set and uppercased."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.illusion_text == "HELLO WORLD"

    def test_default_num_rotations(self, font_path, temp_dir):
        """Test default number of rotations."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.num_rotations == 6

    def test_default_file_ext(self, font_path, temp_dir):
        """Test default file extension."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.file_ext == ".png"

    def test_default_text_color(self, font_path, temp_dir):
        """Test default text color is black."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.text_color == (0, 0, 0)

    def test_default_background_color(self, font_path, temp_dir):
        """Test default background color is white."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.background_color == (255, 255, 255)

    def test_default_img_side(self, font_path, temp_dir):
        """Test default image side length."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.img_side == 1024

    def test_default_charmax(self, font_path, temp_dir):
        """Test default character maximum."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.charmax == 22

    def test_default_crop_widths(self, font_path, temp_dir):
        """Test default crop width values."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.crop_width_x == 14
        assert p.crop_width_y == 5

    def test_default_darkness_threshold(self, font_path, temp_dir):
        """Test default darkness threshold."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.darkness_threshold == 116

    def test_default_upper_case(self, font_path, temp_dir):
        """Test that upper_case defaults to True."""
        p = Pyedgeon(illusion_text="hello", font_path=font_path, file_path=temp_dir)
        assert p.illusion_text == "HELLO"


class TestTextHandling:
    """Test text parameter handling and transformations."""

    def test_uppercase_conversion(self, font_path, temp_dir):
        """Test that text is converted to uppercase by default."""
        p = Pyedgeon(
            illusion_text="hello world",
            font_path=font_path,
            file_path=temp_dir
        )
        assert p.illusion_text == "HELLO WORLD"

    def test_uppercase_disabled(self, font_path, temp_dir):
        """Test that upper_case=False preserves original case."""
        p = Pyedgeon(
            illusion_text="Hello World",
            font_path=font_path,
            file_path=temp_dir,
            upper_case=False
        )
        assert p.illusion_text == "Hello World"

    def test_empty_string(self, font_path, temp_dir):
        """Test that empty string is properly rejected."""
        import pytest
        # Validation now rejects empty strings
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                illusion_text="",
                font_path=font_path,
                file_path=temp_dir
            )

    def test_special_characters(self, font_path, temp_dir):
        """Test handling of special characters."""
        special_text = "HELLO! @#$%"
        p = Pyedgeon(
            illusion_text=special_text,
            font_path=font_path,
            file_path=temp_dir
        )
        assert p.illusion_text == special_text

    def test_unicode_characters(self, font_path, temp_dir):
        """Test handling of unicode characters."""
        unicode_text = "HELLO \u2665"  # Heart symbol
        p = Pyedgeon(
            illusion_text=unicode_text,
            font_path=font_path,
            file_path=temp_dir
        )
        assert p.illusion_text == unicode_text

    def test_numeric_text(self, font_path, temp_dir):
        """Test handling of numeric text."""
        p = Pyedgeon(
            illusion_text="123456",
            font_path=font_path,
            file_path=temp_dir
        )
        assert p.illusion_text == "123456"


class TestColorParameters:
    """Test color parameter validation and handling."""

    def test_custom_text_color(self, font_path, temp_dir):
        """Test setting custom text color."""
        red = (255, 0, 0)
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            text_color=red
        )
        assert p.text_color == red

    def test_custom_background_color(self, font_path, temp_dir):
        """Test setting custom background color."""
        blue = (0, 0, 255)
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            background_color=blue
        )
        assert p.background_color == blue

    def test_grayscale_colors(self, font_path, temp_dir):
        """Test grayscale color values."""
        gray = (128, 128, 128)
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            text_color=gray
        )
        assert p.text_color == gray

    def test_color_boundaries(self, font_path, temp_dir):
        """Test color values at boundaries (0 and 255)."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            text_color=(0, 0, 0),
            background_color=(255, 255, 255)
        )
        assert p.text_color == (0, 0, 0)
        assert p.background_color == (255, 255, 255)


class TestFileParameters:
    """Test file path and naming parameter handling."""

    def test_custom_file_name(self, font_path, temp_dir):
        """Test setting custom file name."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            file_name="custom_name"
        )
        assert p.file_name == "custom_name"

    def test_file_name_defaults_to_text(self, font_path, temp_dir):
        """Test that file_name defaults to illusion_text."""
        p = Pyedgeon(
            illusion_text="TEST TEXT",
            font_path=font_path,
            file_path=temp_dir
        )
        assert p.file_name == "TEST TEXT"

    def test_custom_file_extension(self, font_path, temp_dir):
        """Test setting custom file extension."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            file_ext=".jpg"
        )
        assert p.file_ext == ".jpg"

    def test_empty_file_path(self, font_path):
        """Test that empty file_path is accepted."""
        p = Pyedgeon(font_path=font_path, file_path="")
        assert p.file_path == ""

    def test_custom_file_path(self, font_path, temp_dir):
        """Test setting custom file path."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.file_path == temp_dir


class TestImageSizeParameters:
    """Test image size and dimension parameters."""

    def test_custom_img_side(self, font_path, temp_dir):
        """Test setting custom image side length."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            img_side=512
        )
        assert p.img_side == 512
        assert p.img_size == (512, 512)

    def test_small_image_size(self, font_path, temp_dir):
        """Test with small image size."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            img_side=128
        )
        assert p.img_side == 128

    def test_large_image_size(self, font_path, temp_dir):
        """Test with large image size."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            img_side=2048
        )
        assert p.img_side == 2048

    def test_img_size_tuple_creation(self, font_path, temp_dir):
        """Test that img_size tuple is created correctly."""
        side = 800
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            img_side=side
        )
        assert p.img_size == (side, side)
        assert p.img_size_text == (side, side)


class TestRotationParameters:
    """Test rotation-related parameters."""

    def test_custom_num_rotations(self, font_path, temp_dir):
        """Test setting custom number of rotations."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            num_rotations=8
        )
        assert p.num_rotations == 8

    def test_minimum_rotations(self, font_path, temp_dir):
        """Test with minimum number of rotations."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            num_rotations=1
        )
        assert p.num_rotations == 1

    def test_many_rotations(self, font_path, temp_dir):
        """Test with many rotations."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            num_rotations=12
        )
        assert p.num_rotations == 12


class TestCropParameters:
    """Test crop width parameters."""

    def test_custom_crop_width_x(self, font_path, temp_dir):
        """Test setting custom crop_width_x."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            crop_width_x=20
        )
        assert p.crop_width_x == 20

    def test_custom_crop_width_y(self, font_path, temp_dir):
        """Test setting custom crop_width_y."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            crop_width_y=10
        )
        assert p.crop_width_y == 10

    def test_zero_crop_widths(self, font_path, temp_dir):
        """Test with zero crop widths."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            crop_width_x=0,
            crop_width_y=0
        )
        assert p.crop_width_x == 0
        assert p.crop_width_y == 0


class TestDarknessThreshold:
    """Test darkness threshold parameter."""

    def test_custom_darkness_threshold(self, font_path, temp_dir):
        """Test setting custom darkness threshold."""
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            darkness_threshold=100
        )
        assert p.darkness_threshold == 100

    def test_threshold_boundaries(self, font_path, temp_dir):
        """Test darkness threshold at boundaries."""
        p_low = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            darkness_threshold=0
        )
        assert p_low.darkness_threshold == 0

        p_high = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            darkness_threshold=255
        )
        assert p_high.darkness_threshold == 255


class TestInitialState:
    """Test the initial state of Pyedgeon object after construction."""

    def test_font_size_initially_none(self, font_path, temp_dir):
        """Test that font_size is None before calculation."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.font_size is None

    def test_font_size_guess_initially_none(self, font_path, temp_dir):
        """Test that font_size_guess is None before estimation."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)
        assert p.font_size_guess is None

    def test_all_required_attributes_exist(self, font_path, temp_dir):
        """Test that all expected attributes are set after initialization."""
        p = Pyedgeon(font_path=font_path, file_path=temp_dir)

        required_attrs = [
            'illusion_text', 'font_path', 'num_rotations', 'file_ext',
            'text_color', 'background_color', 'img_side', 'charmax',
            'file_path', 'font_size_guess', 'crop_width_x', 'crop_width_y',
            'darkness_threshold', 'img_size', 'img_size_text', 'file_name',
            'font_size'
        ]

        for attr in required_attrs:
            assert hasattr(p, attr), f"Missing attribute: {attr}"
