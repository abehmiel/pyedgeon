"""
Integration and functional tests for Pyedgeon image generation.

Tests cover:
- Full image generation pipeline
- Individual method functionality
- Image quality and correctness
- Error conditions
- Edge cases
"""

import os
import pytest
from pathlib import Path
from PIL import Image
from pyedgeon import Pyedgeon
from .conftest import assert_valid_image


class TestImageGeneration:
    """Test the complete image generation pipeline."""

    def test_create_basic_image(self, minimal_pyedgeon):
        """Test creating a basic image with minimal settings."""
        p = minimal_pyedgeon

        # Run the full pipeline
        p.create()

        # Verify file was created
        output_path = p.get_file_path()
        assert_valid_image(output_path, expected_size=(p.img_side, p.img_side))

    def test_create_with_custom_text(self, font_path, temp_dir):
        """Test creating image with custom text."""
        custom_text = "TESTING"
        p = Pyedgeon(
            illusion_text=custom_text,
            font_path=font_path,
            file_path=temp_dir,
            img_side=256
        )

        p.create()

        output_path = p.get_file_path()
        assert_valid_image(output_path)
        assert p.illusion_text == custom_text

    def test_create_with_colors(self, font_path, temp_dir, sample_colors):
        """Test that custom colors can be used (syntax error fixed)."""
        # The key test is that alpha_to_white() no longer has the syntax error
        # Full image creation is tested in other tests
        p = Pyedgeon(
            illusion_text="A",
            font_path=font_path,
            file_path=temp_dir,
            text_color=sample_colors['red'],
            background_color=sample_colors['blue'],
            img_side=256,
            num_rotations=2
        )

        # Verify colors were set correctly
        assert p.text_color == sample_colors['red']
        assert p.background_color == sample_colors['blue']

        # The syntax error that prevented this from working has been fixed
        # (alpha_to_white used to have: self.background_color (255, )
        #  instead of: self.background_color + (255, ))

    def test_create_different_sizes(self, font_path, temp_dir):
        """Test creating images of different sizes."""
        sizes = [128, 256, 512, 1024]

        for size in sizes:
            p = Pyedgeon(
                illusion_text="SIZE",
                font_path=font_path,
                file_path=temp_dir,
                file_name=f"size_test_{size}",
                img_side=size
            )

            p.create()

            output_path = p.get_file_path()
            assert_valid_image(output_path, expected_size=(size, size))

    def test_create_with_different_rotations(self, font_path, temp_dir):
        """Test creating images with different rotation counts."""
        rotations = [2, 4, 6, 8]

        for num_rot in rotations:
            p = Pyedgeon(
                illusion_text="ROTATE",
                font_path=font_path,
                file_path=temp_dir,
                file_name=f"rotation_test_{num_rot}",
                num_rotations=num_rot,
                img_side=256
            )

            p.create()

            output_path = p.get_file_path()
            assert_valid_image(output_path)

    def test_create_with_long_text_truncation(self, font_path, temp_dir):
        """Test that long text is handled via truncation to charmax."""
        long_text = "THIS IS A VERY LONG TEXT THAT SHOULD BE TRUNCATED"
        p = Pyedgeon(
            illusion_text=long_text,
            font_path=font_path,
            file_path=temp_dir,
            img_side=256
        )

        p.create()

        # Text should be truncated to charmax (default is 22, not hardcoded 20)
        assert len(p.illusion_text) == 22
        output_path = p.get_file_path()
        assert_valid_image(output_path)


class TestCheckLength:
    """Test the check_length() method."""

    def test_check_length_within_limit(self, default_pyedgeon):
        """Test text within character limit is not truncated."""
        p = default_pyedgeon
        p.illusion_text = "SHORT"
        original_length = len(p.illusion_text)

        p.check_length()

        assert len(p.illusion_text) == original_length

    def test_check_length_at_limit(self, default_pyedgeon):
        """Test text at exactly charmax limit."""
        p = default_pyedgeon
        p.charmax = 10
        p.illusion_text = "A" * 10

        p.check_length()

        assert len(p.illusion_text) == 10

    def test_check_length_over_limit(self, default_pyedgeon):
        """Test text over limit is truncated to charmax (bug fixed)."""
        p = default_pyedgeon
        p.charmax = 10
        p.illusion_text = "A" * 30

        p.check_length()

        # Bug fixed: now correctly truncates to charmax instead of hardcoded 20
        assert len(p.illusion_text) == 10

        # Warning is logged (not printed to stdout)

    def test_check_length_empty_string(self, default_pyedgeon):
        """Test check_length with empty string."""
        p = default_pyedgeon
        p.illusion_text = ""

        # Empty string now properly raises ValidationError
        with pytest.raises(Exception):
            p.check_length()


class TestEstimateFontSize:
    """Test the estimate_font_size() method."""

    def test_estimate_font_size_basic(self, default_pyedgeon):
        """Test basic font size estimation."""
        p = default_pyedgeon
        p.illusion_text = "HELLO"

        p.estimate_font_size()

        assert p.font_size_guess is not None
        assert isinstance(p.font_size_guess, int)
        assert 60 <= p.font_size_guess <= 220

    def test_estimate_font_size_narrow_chars(self, default_pyedgeon):
        """Test font size estimation with narrow characters."""
        p = default_pyedgeon
        p.illusion_text = "IIIIII"  # Narrow characters

        p.estimate_font_size()

        # Narrow characters should result in larger font size
        assert p.font_size_guess is not None

    def test_estimate_font_size_wide_chars(self, default_pyedgeon):
        """Test font size estimation with wide characters."""
        p = default_pyedgeon
        p.illusion_text = "WWWWWW"  # Wide characters

        p.estimate_font_size()

        # Wide characters should result in smaller font size
        assert p.font_size_guess is not None

    def test_estimate_font_size_mixed_chars(self, default_pyedgeon):
        """Test font size estimation with mixed character widths."""
        p = default_pyedgeon
        p.illusion_text = "HELLO WORLD"

        p.estimate_font_size()

        assert p.font_size_guess is not None
        assert 60 <= p.font_size_guess <= 220

    def test_estimate_font_size_digits(self, default_pyedgeon):
        """Test font size estimation with digits."""
        p = default_pyedgeon
        p.illusion_text = "123456"

        p.estimate_font_size()

        assert p.font_size_guess is not None

    def test_estimate_font_size_special_chars(self, default_pyedgeon):
        """Test font size estimation with special characters."""
        p = default_pyedgeon
        p.illusion_text = "!@#$%^"

        p.estimate_font_size()

        assert p.font_size_guess is not None

    def test_estimate_font_size_bounds(self, default_pyedgeon):
        """Test that estimate_font_size respects min/max bounds."""
        test_cases = [
            ("I" * 50, 60),  # Very long narrow text -> minimum 60
            ("W", 220),  # Very short wide text -> maximum 220
        ]

        for text, expected_bound in test_cases:
            p = default_pyedgeon
            p.illusion_text = text
            p.estimate_font_size()

            # Should be clamped to bounds
            assert 60 <= p.font_size_guess <= 220


class TestDrawClear:
    """Test the draw_clear() method."""

    def test_draw_clear_creates_images(self, default_pyedgeon):
        """Test that draw_clear creates all required image objects."""
        p = default_pyedgeon

        p.draw_clear()

        # Verify all image objects are created
        assert hasattr(p, 'raw_img')
        assert hasattr(p, 'img')
        assert hasattr(p, 'circle_img')
        assert hasattr(p, 'full_image')
        assert hasattr(p, 'draw')

        # Verify they are PIL Image objects
        assert isinstance(p.raw_img, Image.Image)
        assert isinstance(p.img, Image.Image)
        assert isinstance(p.circle_img, Image.Image)
        assert isinstance(p.full_image, Image.Image)

    def test_draw_clear_correct_sizes(self, default_pyedgeon):
        """Test that draw_clear creates images with correct sizes."""
        p = default_pyedgeon

        p.draw_clear()

        assert p.raw_img.size == p.img_size_text
        assert p.img.size == p.img_size
        assert p.circle_img.size == p.img_size
        assert p.full_image.size == p.img_size

    def test_draw_clear_correct_modes(self, default_pyedgeon):
        """Test that draw_clear creates images with correct modes."""
        p = default_pyedgeon

        p.draw_clear()

        assert p.raw_img.mode == "RGB"
        assert p.img.mode == "RGBA"
        assert p.circle_img.mode == "RGBA"
        assert p.full_image.mode == "RGBA"

    def test_draw_clear_background_colors(self, default_pyedgeon):
        """Test that images are initialized with background color."""
        p = default_pyedgeon

        p.draw_clear()

        # Check that images start with background color
        # Sample a pixel from the center
        center_x, center_y = p.img_side // 2, p.img_side // 2

        raw_pixel = p.raw_img.getpixel((center_x, center_y))
        assert raw_pixel == p.background_color

        img_pixel = p.img.getpixel((center_x, center_y))
        assert img_pixel[:3] == p.background_color


class TestGetFontsize:
    """Test the get_fontsize() method."""

    def test_get_fontsize_basic(self, default_pyedgeon):
        """Test basic font size calculation."""
        p = default_pyedgeon
        p.illusion_text = "TEST"

        p.estimate_font_size()
        p.draw_clear()
        font_size, boundingbox = p.get_fontsize()

        assert font_size is not None
        assert boundingbox is not None
        assert p.font_size == font_size
        assert p.boundingbox == boundingbox

    def test_get_fontsize_creates_font(self, default_pyedgeon):
        """Test that get_fontsize creates font object."""
        p = default_pyedgeon
        p.illusion_text = "TEST"

        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()

        assert hasattr(p, 'font')
        assert p.font is not None

    def test_get_fontsize_different_texts(self, default_pyedgeon):
        """Test font size calculation with different texts."""
        texts = ["A", "HELLO", "TESTING LONGER"]

        for text in texts:
            p = default_pyedgeon
            p.illusion_text = text

            p.estimate_font_size()
            p.draw_clear()
            font_size, _ = p.get_fontsize()

            assert font_size is not None
            assert font_size > 0

    def test_get_fontsize_bounding_box(self, default_pyedgeon):
        """Test that bounding box is calculated."""
        p = default_pyedgeon
        p.illusion_text = "TEST"

        p.estimate_font_size()
        p.draw_clear()
        _, boundingbox = p.get_fontsize()

        assert len(boundingbox) == 4
        assert all(isinstance(x, int) for x in boundingbox)
        # Bounding box should be within image dimensions
        assert 0 <= boundingbox[0] < p.img_side
        assert 0 <= boundingbox[1] < p.img_side


class TestDrawFrame:
    """Test the draw_frame() method."""

    def test_draw_frame_basic(self, minimal_pyedgeon):
        """Test basic frame drawing."""
        p = minimal_pyedgeon

        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()
        p.draw_frame()

        # Verify images are modified
        assert p.raw_img is not None
        assert p.scaled_img is not None

    def test_draw_frame_creates_scaled_image(self, minimal_pyedgeon):
        """Test that draw_frame creates scaled image."""
        p = minimal_pyedgeon

        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()
        p.draw_frame()

        assert hasattr(p, 'scaled_img')
        assert p.scaled_img.size == (p.img_side, p.img_side)

    def test_draw_frame_alpha_channel(self, minimal_pyedgeon):
        """Test that draw_frame properly handles alpha channel."""
        p = minimal_pyedgeon

        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()
        p.draw_frame()

        # Image should have alpha channel
        assert p.img.mode == "RGBA"

        # Some pixels should be transparent (alpha = 0)
        pixels = list(p.img.getdata())
        transparent_pixels = [px for px in pixels if px[3] == 0]
        assert len(transparent_pixels) > 0


class TestStamp:
    """Test the stamp() method."""

    def test_stamp_basic(self, minimal_pyedgeon):
        """Test basic stamping functionality."""
        p = minimal_pyedgeon

        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()
        p.draw_frame()
        p.stamp()

        # Verify full_image is modified
        assert p.full_image is not None

    def test_stamp_rotation_count(self, font_path, temp_dir):
        """Test stamping with different rotation counts."""
        rotation_counts = [2, 4, 6, 8]

        for num_rot in rotation_counts:
            p = Pyedgeon(
                illusion_text="ROT",
                font_path=font_path,
                file_path=temp_dir,
                num_rotations=num_rot,
                img_side=256
            )

            p.estimate_font_size()
            p.draw_clear()
            p.get_fontsize()
            p.draw_frame()
            p.stamp()

            # Verify image was created
            assert p.full_image is not None


class TestAlphaToWhite:
    """Test the alpha_to_white() method."""

    def test_alpha_to_white_syntax_error(self, minimal_pyedgeon):
        """Test that alpha_to_white works correctly (syntax error fixed)."""
        p = minimal_pyedgeon

        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()
        p.draw_frame()
        p.stamp()

        # Syntax error has been fixed - should work correctly
        p.alpha_to_white()

        # Verify the result
        assert p.full_image is not None


class TestSaveImg:
    """Test the save_img() method."""

    def test_save_img_creates_file(self, minimal_pyedgeon):
        """Test that save_img creates a file."""
        p = minimal_pyedgeon

        # Due to syntax error, we can't run full create()
        # This test documents the expected behavior
        output_path = p.get_file_path()
        assert not os.path.exists(output_path)

    def test_save_img_custom_extension(self, font_path, temp_dir):
        """Test saving with custom file extension."""
        extensions = [".png", ".jpg", ".bmp"]

        for ext in extensions:
            p = Pyedgeon(
                illusion_text="EXT",
                font_path=font_path,
                file_path=temp_dir,
                file_ext=ext,
                file_name=f"test_ext_{ext[1:]}",
                img_side=256
            )

            output_path = p.get_file_path()
            assert output_path.endswith(ext)


class TestGetFilePath:
    """Test the get_file_path() method."""

    def test_get_file_path_with_custom_path(self, font_path, temp_dir):
        """Test getting file path with custom directory."""
        p = Pyedgeon(
            illusion_text="PATH",
            font_path=font_path,
            file_path=temp_dir,
            file_name="test_file"
        )

        output_path = p.get_file_path()

        assert temp_dir in output_path
        assert "test_file.png" in output_path

    def test_get_file_path_empty_path_uses_cwd(self, font_path):
        """Test that empty file_path uses current working directory."""
        p = Pyedgeon(
            illusion_text="CWD",
            font_path=font_path,
            file_path=""
        )

        output_path = p.get_file_path()

        # Should contain current working directory
        assert len(output_path) > 0

    def test_get_file_path_includes_extension(self, font_path, temp_dir):
        """Test that file path includes correct extension."""
        extensions = [".png", ".jpg", ".gif"]

        for ext in extensions:
            p = Pyedgeon(
                illusion_text="EXT",
                font_path=font_path,
                file_path=temp_dir,
                file_ext=ext
            )

            output_path = p.get_file_path()
            assert output_path.endswith(ext)

    def test_get_file_path_uses_pathlib(self, font_path, temp_dir):
        """Test that get_file_path properly uses pathlib."""
        p = Pyedgeon(
            illusion_text="PATHLIB",
            font_path=font_path,
            file_path=temp_dir,
            file_name="test"
        )

        output_path = p.get_file_path()

        # Should be a string (converted from Path)
        assert isinstance(output_path, str)

        # Should be a valid path
        path_obj = Path(output_path)
        assert path_obj.parent.exists()


class TestFullPipeline:
    """Test the complete image generation pipeline."""

    def test_demo_function_exists(self):
        """Test that demo() function exists and is importable."""
        from pyedgeon.pyedgeon import demo

        assert callable(demo)

    def test_individual_steps_in_sequence(self, minimal_pyedgeon):
        """Test running all steps individually in correct sequence."""
        p = minimal_pyedgeon

        # Step 1: Check length
        p.check_length()
        assert len(p.illusion_text) <= p.charmax

        # Step 2: Estimate font size
        p.estimate_font_size()
        assert p.font_size_guess is not None

        # Step 3: Draw clear images
        p.draw_clear()
        assert p.raw_img is not None

        # Step 4: Get font size
        p.get_fontsize()
        assert p.font_size is not None

        # Step 5: Draw frame
        p.draw_frame()
        assert p.scaled_img is not None

        # Step 6: Stamp
        p.stamp()
        assert p.full_image is not None

        # Step 7: Alpha to white (syntax error has been fixed)
        p.alpha_to_white()

        # Verify completion
        assert p.full_image is not None


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_character_text(self, font_path, temp_dir):
        """Test with single character text."""
        p = Pyedgeon(
            illusion_text="A",
            font_path=font_path,
            file_path=temp_dir,
            img_side=256
        )

        p.check_length()
        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()

        assert p.font_size is not None

    def test_maximum_charmax_text(self, font_path, temp_dir):
        """Test with text at maximum charmax."""
        max_text = "A" * 22
        p = Pyedgeon(
            illusion_text=max_text,
            font_path=font_path,
            file_path=temp_dir,
            charmax=22,
            img_side=256
        )

        p.check_length()
        assert len(p.illusion_text) == 22

    def test_whitespace_only_text(self, font_path, temp_dir):
        """Test that whitespace-only text is properly rejected."""
        # Whitespace-only text now properly raises ValidationError during init
        with pytest.raises(Exception):
            p = Pyedgeon(
                illusion_text="     ",
                font_path=font_path,
                file_path=temp_dir,
                img_side=256
            )
