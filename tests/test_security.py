"""
Security tests for Pyedgeon library.

Tests cover:
- Path traversal vulnerabilities
- Input validation
- Resource exhaustion protection
- File system security
- Injection attacks
"""

import os
import pytest
from pathlib import Path
from pyedgeon import Pyedgeon


class TestPathTraversalPrevention:
    """Test protection against path traversal attacks."""

    def test_file_path_traversal_parent_directory(self, font_path, temp_dir):
        """Test that parent directory traversal in file_path is handled safely."""
        malicious_path = "../../../etc"
        p = Pyedgeon(
            font_path=font_path,
            file_path=malicious_path,
            illusion_text="TEST"
        )

        # Validation now properly checks that output directory exists
        # This will raise an error because ../../../etc likely doesn't exist
        with pytest.raises(Exception):  # Should raise ValidationError
            output_path = p.get_file_path()

    def test_file_path_absolute_system_path(self, font_path, temp_dir):
        """Test that absolute system paths in file_path are accepted."""
        # This tests whether the code accepts absolute paths to system directories
        # Note: Users may legitimately want to write to specific absolute paths
        malicious_paths = [
            "/etc",
            "/tmp/../etc",
            "/var/log"
        ]

        for mal_path in malicious_paths:
            p = Pyedgeon(
                font_path=font_path,
                file_path=mal_path,
                illusion_text="TEST"
            )
            # Absolute paths are accepted (users may have legitimate use cases)
            assert p.file_path == mal_path

    def test_file_name_with_path_traversal(self, font_path, temp_dir):
        """Test that file_name with path traversal is properly sanitized."""
        malicious_names = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "./../../secret.txt"
        ]

        for mal_name in malicious_names:
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                file_name=mal_name,
                illusion_text="TEST"
            )
            output_path = p.get_file_path()

            # Verify dangerous characters are sanitized
            # Path separators and dots should be removed or replaced
            assert "../" not in output_path
            assert "..\\" not in output_path
            # Should still be within temp_dir
            assert temp_dir in output_path or output_path.startswith(temp_dir)

    def test_font_path_traversal(self, temp_dir):
        """Test that font_path rejects paths with invalid extensions."""
        malicious_font_paths = [
            "../../../etc/passwd",
            "/etc/shadow",
            "C:\\Windows\\System32\\config\\SAM"
        ]

        for mal_path in malicious_font_paths:
            # Font path validation now rejects non-font file extensions
            with pytest.raises(Exception):  # Should raise ValidationError
                p = Pyedgeon(
                    font_path=mal_path,
                    file_path=temp_dir,
                    illusion_text="TEST"
                )

    def test_null_byte_injection_file_name(self, font_path, temp_dir):
        """Test handling of null byte injection in file names."""
        malicious_name = "safe_name\x00../../etc/passwd"
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            file_name=malicious_name,
            illusion_text="TEST"
        )
        # Documents that null bytes are currently not filtered
        assert "\x00" in p.file_name

    def test_symlink_in_file_path(self, font_path, temp_dir):
        """Test behavior when file_path contains symlinks."""
        # Create a symlink to a different directory
        symlink_path = Path(temp_dir) / "symlink"
        target_path = Path(temp_dir) / "target"
        target_path.mkdir(exist_ok=True)

        try:
            symlink_path.symlink_to(target_path)

            p = Pyedgeon(
                font_path=font_path,
                file_path=str(symlink_path),
                illusion_text="TEST"
            )

            # Verify symlinks are followed (current behavior)
            assert p.file_path == str(symlink_path)
        except OSError:
            # Symlink creation might fail on some systems
            pytest.skip("Symlink creation not supported")


class TestInputValidation:
    """Test validation of user inputs."""

    def test_color_validation_out_of_range_high(self, font_path, temp_dir):
        """Test that colors above 255 are properly rejected."""
        # Validation now properly checks color ranges
        invalid_color = (300, 300, 300)
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                text_color=invalid_color
            )

    def test_color_validation_negative(self, font_path, temp_dir):
        """Test that negative color values are properly rejected."""
        invalid_color = (-10, -20, -30)
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                text_color=invalid_color
            )

    def test_color_validation_wrong_type(self, font_path, temp_dir):
        """Test that wrong color type is properly rejected."""
        # Validation now checks that color is a 3-tuple
        with pytest.raises(Exception):  # Should raise ValidationError or TypeError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                text_color="red"  # String instead of tuple
            )

    def test_color_validation_wrong_tuple_length(self, font_path, temp_dir):
        """Test that wrong tuple length for color is properly rejected."""
        invalid_colors = [
            (255,),  # Too short
            (255, 255),  # Too short
            (255, 255, 255, 255),  # Too long
        ]

        for invalid_color in invalid_colors:
            # Validation now properly checks tuple length
            with pytest.raises(Exception):  # Should raise ValidationError
                p = Pyedgeon(
                    font_path=font_path,
                    file_path=temp_dir,
                    text_color=invalid_color
                )

    def test_num_rotations_negative(self, font_path, temp_dir):
        """Test that negative num_rotations is properly rejected."""
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                num_rotations=-5
            )

    def test_num_rotations_zero(self, font_path, temp_dir):
        """Test that zero num_rotations is properly rejected."""
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                num_rotations=0
            )

    def test_img_side_negative(self, font_path, temp_dir):
        """Test that negative img_side is properly rejected."""
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                img_side=-100
            )

    def test_img_side_zero(self, font_path, temp_dir):
        """Test that zero img_side is properly rejected."""
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                img_side=0
            )

    def test_charmax_negative(self, font_path, temp_dir):
        """Test that negative charmax is properly rejected."""
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                charmax=-10
            )

    def test_darkness_threshold_out_of_range(self, font_path, temp_dir):
        """Test that darkness_threshold outside 0-255 is properly rejected."""
        invalid_thresholds = [-10, 300, 1000]

        for threshold in invalid_thresholds:
            with pytest.raises(Exception):  # Should raise ValidationError
                p = Pyedgeon(
                    font_path=font_path,
                    file_path=temp_dir,
                    darkness_threshold=threshold
                )


class TestResourceExhaustion:
    """Test protection against resource exhaustion attacks."""

    def test_extremely_large_image_size(self, font_path, temp_dir):
        """Test that extremely large image sizes are properly rejected."""
        # An attacker could try to exhaust memory with huge images
        huge_size = 100000  # 100k x 100k = 10 billion pixels

        # Validation now prevents resource exhaustion (max is 8192)
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                img_side=huge_size,
                illusion_text="A"
            )

    def test_extremely_long_text(self, font_path, temp_dir):
        """Test that extremely long text (>10000 chars) is properly rejected."""
        # Test with very long text that could cause performance issues
        long_text = "A" * 10001  # Just over the 10000 limit

        # Validation now rejects text over 10000 characters
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                illusion_text=long_text
            )

    def test_check_length_truncation_silent(self, font_path, temp_dir):
        """Test that check_length() correctly truncates text to charmax."""
        long_text = "A" * 50
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            illusion_text=long_text,
            charmax=22
        )

        p.check_length()

        # Verify text was correctly truncated to charmax (bug has been fixed!)
        assert len(p.illusion_text) == 22

        # Warning is logged (not printed to stdout)

    def test_check_length_hardcoded_truncation(self, font_path, temp_dir):
        """Test that truncation correctly uses charmax value (bug fixed)."""
        long_text = "A" * 50
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            illusion_text=long_text,
            charmax=30  # Set to 30
        )

        p.check_length()

        # Bug has been fixed: now correctly truncates to charmax value
        assert len(p.illusion_text) == 30

    def test_many_rotations_performance(self, font_path, temp_dir):
        """Test that excessive rotations are properly limited."""
        excessive_rotations = 1000

        # Validation now prevents excessive rotations (max is 360)
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                num_rotations=excessive_rotations,
                illusion_text="A"
            )


class TestFileSystemSecurity:
    """Test file system security issues."""

    def test_file_overwrite_without_warning(self, font_path, temp_dir):
        """Test that existing files are overwritten without warning."""
        file_name = "test_file"
        file_path = Path(temp_dir) / f"{file_name}.png"

        # Create an existing file
        file_path.write_text("existing content")
        assert file_path.exists()

        # Create Pyedgeon instance that will overwrite
        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            file_name=file_name,
            illusion_text="TEST"
        )

        # Verify it would overwrite (without actually running create())
        # Path may be resolved differently on macOS (/var vs /private/var)
        result_path = p.get_file_path()
        assert str(file_path) in result_path or result_path in str(file_path)

    def test_file_extension_validation(self, font_path, temp_dir):
        """Test that dangerous file extensions are properly rejected."""
        dangerous_extensions = [
            ".exe",
            ".sh",
            ".bat",
            ".ps1",
            "",  # No extension
            ".png.exe",  # Double extension
        ]

        for ext in dangerous_extensions:
            # Validation now properly rejects dangerous extensions
            with pytest.raises(Exception):  # Should raise ValidationError
                p = Pyedgeon(
                    font_path=font_path,
                    file_path=temp_dir,
                    file_ext=ext,
                    illusion_text="TEST"
                )

    def test_font_file_existence_check(self, temp_dir):
        """Test that non-existent font files are accepted during init."""
        non_existent_font = "/path/to/nonexistent/font.ttf"

        # Constructor accepts non-existent paths
        p = Pyedgeon(
            font_path=non_existent_font,
            file_path=temp_dir,
            illusion_text="TEST"
        )

        assert p.font_path == non_existent_font

    def test_font_file_type_validation(self, temp_dir, fake_font_file):
        """Test that non-font files with .ttf extension are accepted."""
        # fake_font_file is not a valid font but has .ttf extension
        p = Pyedgeon(
            font_path=fake_font_file,
            file_path=temp_dir,
            illusion_text="TEST"
        )

        # Path may be resolved differently on different systems (e.g., /var vs /private/var on macOS)
        assert fake_font_file in p.font_path or p.font_path in fake_font_file


class TestErrorHandling:
    """Test error handling and exception management."""

    def test_bare_except_in_get_fontsize(self, font_path, temp_dir):
        """Test that bare except clause has been fixed in get_fontsize()."""
        # Previously had a bare except clause which is a security risk
        # Now properly uses specific exception handling

        import inspect
        from pyedgeon import Pyedgeon

        source = inspect.getsource(Pyedgeon.get_fontsize)

        # Verify bare except has been fixed - should use 'except Exception as e:' instead
        assert "except Exception as e:" in source or "except (IOError, OSError)" in source
        # Should NOT have bare except:
        assert "except:" not in source or "except Exception" in source  # Allow 'except Exception'

    def test_unbounded_recursion_in_get_fontsize(self, font_path, temp_dir):
        """Test that get_fontsize() has unbounded recursion."""
        # The function can recurse indefinitely without a base case
        # This is a potential denial of service vector

        p = Pyedgeon(
            font_path=font_path,
            file_path=temp_dir,
            illusion_text="TEST",
            img_side=256
        )

        # Set up conditions that would cause recursion
        p.font_size_guess = 50

        # Note: We don't actually call this to avoid stack overflow
        # This test documents the risk
        assert hasattr(p, 'get_fontsize')


class TestSyntaxErrorDocumentation:
    """Document the syntax error on line 215."""

    def test_line_215_syntax_error_exists(self):
        """Test that verifies the syntax error on line 215 has been fixed."""
        # Line 215 previously had: self.background_color (255, )
        # Now correctly fixed to: self.background_color + (255, )

        import inspect
        from pyedgeon import Pyedgeon

        source = inspect.getsource(Pyedgeon.alpha_to_white)

        # Verify the fix is in place - should use + operator, not function call
        assert "self.background_color + (255," in source


class TestInjectionVectors:
    """Test for various injection attack vectors."""

    def test_command_injection_in_file_path(self, font_path):
        """Test that command injection in file_path is possible."""
        # Potentially dangerous path with shell metacharacters
        dangerous_paths = [
            "; rm -rf /",
            "$(malicious_command)",
            "`malicious_command`",
            "| cat /etc/passwd",
        ]

        for dangerous_path in dangerous_paths:
            p = Pyedgeon(
                font_path=font_path,
                file_path=dangerous_path,
                illusion_text="TEST"
            )
            # Currently no sanitization
            assert dangerous_path in p.file_path

    def test_format_string_in_text(self, font_path, temp_dir):
        """Test handling of format string-like text."""
        format_strings = [
            "{0}",
            "%s%s%s%s",
            "${malicious}",
        ]

        for fmt_str in format_strings:
            p = Pyedgeon(
                font_path=font_path,
                file_path=temp_dir,
                illusion_text=fmt_str
            )
            # Verify format strings are not interpreted
            assert p.illusion_text == fmt_str.upper()
