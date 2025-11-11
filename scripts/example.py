#!/usr/bin/env python3
"""
Quick-start example for pyedgeon.

This script demonstrates how to create a simple pyedgeon button
with customizable message, font, and output filename.

Usage:
    python example.py
    python example.py "CUSTOM TEXT"
    python example.py "CUSTOM TEXT" --font /path/to/font.ttf
    python example.py "CUSTOM TEXT" --output my_image.png

Or via Makefile:
    make example
    make example MESSAGE="CUSTOM TEXT"
"""

import argparse
import sys
from pathlib import Path
from pyedgeon import Pyedgeon


def main():
    """Create a pyedgeon image with command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a pyedgeon optical illusion image",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s "HELLO WORLD"
  %(prog)s "SECRET MESSAGE" --font /System/Library/Fonts/Helvetica.ttc
  %(prog)s "COOL DESIGN" --output cool.png
        """
    )

    parser.add_argument(
        'message',
        nargs='?',
        default='HELLO WORLD',
        help='Text message to encode in the illusion (default: "HELLO WORLD")'
    )

    parser.add_argument(
        '--font',
        '--font-path',
        dest='font_path',
        default=None,
        help='Path to TrueType font file (auto-detected if not specified)'
    )

    parser.add_argument(
        '--output',
        '--output-filename',
        dest='output_filename',
        default=None,
        help='Output filename (default: based on message text)'
    )

    parser.add_argument(
        '--size',
        '--img-size',
        dest='img_size',
        type=int,
        default=1024,
        help='Image size in pixels (default: 1024)'
    )

    parser.add_argument(
        '--rotations',
        type=int,
        default=6,
        help='Number of text rotations (default: 6)'
    )

    args = parser.parse_args()

    # Prepare parameters
    message = args.message
    font_path = args.font_path
    img_size = args.img_size
    rotations = args.rotations

    # Handle output filename
    if args.output_filename:
        # Extract filename and extension
        output_path = Path(args.output_filename)
        file_name = output_path.stem
        file_ext = output_path.suffix if output_path.suffix else '.png'
    else:
        file_name = None  # Will use message as filename
        file_ext = '.png'

    # Print configuration
    print(f"Creating pyedgeon image...")
    print(f"  Message: {message}")
    if font_path:
        print(f"  Font: {font_path}")
    else:
        print(f"  Font: Auto-detecting system font")
    print(f"  Image size: {img_size}x{img_size}")
    print(f"  Rotations: {rotations}")

    try:
        # Create the image
        img = Pyedgeon(
            illusion_text=message,
            font_path=font_path,
            file_name=file_name,
            file_ext=file_ext,
            img_side=img_size,
            num_rotations=rotations
        )
        img.create()

        output_file = img.get_file_path()
        print(f"\nSuccess! Image saved to: {output_file}")
        print(f"\nTip: View the image on a mobile device or tilt your screen")
        print(f"     to nearly edge-on to see the hidden message!")

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
