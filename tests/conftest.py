"""
Pytest configuration and shared fixtures for pyedgeon test suite.

This module provides common test fixtures, utilities, and configuration
for all test modules in the pyedgeon test suite.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest
from PIL import Image

# Add parent directory to path to import pyedgeon
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyedgeon import Pyedgeon


@pytest.fixture
def temp_dir():
    """
    Provides a temporary directory for test file outputs.
    Automatically cleaned up after test completion.
    """
    temp_path = tempfile.mkdtemp()
    yield temp_path
    # Cleanup after test
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


@pytest.fixture
def font_path():
    """
    Provides a path to a TrueType font for testing.
    Users must provide their own font file - pyedgeon does not bundle fonts.

    Tests will be skipped if no suitable font is found.
    Looks for fonts in common system locations.
    """
    # Check common system font locations
    possible_fonts = [
        # macOS
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
        # Windows
        "C:\\Windows\\Fonts\\arial.ttf",
    ]

    for font_file in possible_fonts:
        if Path(font_file).exists():
            return str(font_file)

    pytest.skip("No suitable system font found for testing. Pyedgeon does not bundle fonts.")


@pytest.fixture
def default_pyedgeon(font_path, temp_dir):
    """
    Creates a Pyedgeon instance with safe default settings for testing.
    Uses the bundled font and a temporary directory.
    """
    return Pyedgeon(
        illusion_text="TEST",
        font_path=font_path,
        file_path=temp_dir,
        num_rotations=6,
        img_side=512  # Smaller for faster tests
    )


@pytest.fixture
def minimal_pyedgeon(font_path, temp_dir):
    """
    Creates a minimal Pyedgeon instance for quick tests.
    Uses smallest viable settings for performance.
    """
    return Pyedgeon(
        illusion_text="HI",
        font_path=font_path,
        file_path=temp_dir,
        num_rotations=2,
        img_side=256  # Very small for speed
    )


@pytest.fixture
def sample_colors():
    """
    Provides a set of valid color tuples for testing.
    """
    return {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'gray': (128, 128, 128),
    }


@pytest.fixture
def fake_font_file(temp_dir):
    """
    Creates a fake (non-functional) font file for path validation testing.
    """
    fake_font = Path(temp_dir) / "fake_font.ttf"
    fake_font.write_bytes(b"not a real font")
    return str(fake_font)


@pytest.fixture
def malicious_paths():
    """
    Provides a collection of potentially malicious file paths for security testing.
    """
    return [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "/etc/shadow",
        "C:\\Windows\\System32\\config\\SAM",
        "./../sensitive_data.txt",
        "~/../../root/.ssh/id_rsa",
        "file:///etc/passwd",
        "\x00malicious.txt",  # Null byte injection
        "normal_path\x00../../etc/passwd",
    ]


@pytest.fixture
def long_text_samples():
    """
    Provides text samples of various lengths for boundary testing.
    """
    return {
        'empty': '',
        'single': 'A',
        'normal': 'HELLO WORLD',
        'max_length': 'A' * 22,
        'over_limit': 'A' * 50,
        'very_long': 'A' * 1000,
    }


def assert_valid_image(file_path, expected_size=None):
    """
    Helper function to assert that a file is a valid image.

    Args:
        file_path: Path to the image file
        expected_size: Optional tuple (width, height) to verify image dimensions
    """
    assert os.path.exists(file_path), f"Image file does not exist: {file_path}"
    assert os.path.getsize(file_path) > 0, f"Image file is empty: {file_path}"

    # Try to open with PIL to verify it's a valid image
    try:
        with Image.open(file_path) as img:
            if expected_size:
                assert img.size == expected_size, \
                    f"Image size {img.size} does not match expected {expected_size}"
            # Verify image is not completely blank
            extrema = img.convert('L').getextrema()
            assert extrema[0] != extrema[1] or extrema[0] != 255, \
                "Image appears to be completely blank"
    except Exception as e:
        pytest.fail(f"Failed to validate image {file_path}: {e}")


def count_pixels_by_color(image, color):
    """
    Counts the number of pixels of a specific color in an image.

    Args:
        image: PIL Image object
        color: Tuple of RGB values

    Returns:
        int: Count of pixels matching the color
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    pixels = list(image.getdata())
    return pixels.count(color)


# Export helper functions so tests can use them
__all__ = ['assert_valid_image', 'count_pixels_by_color']
