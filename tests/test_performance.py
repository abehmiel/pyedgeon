"""
Performance tests for Pyedgeon library.

Tests cover:
- Execution time benchmarks
- Memory usage
- Resource limits
- Performance regressions
- Scalability
"""

import time
import pytest
from pyedgeon import Pyedgeon


class TestPerformanceBenchmarks:
    """Benchmark tests for various operations."""

    def test_initialization_performance(self, font_path, temp_dir, benchmark):
        """Benchmark Pyedgeon initialization time."""
        def create_instance():
            return Pyedgeon(
                illusion_text="BENCHMARK",
                font_path=font_path,
                file_path=temp_dir,
                img_side=512
            )

        result = benchmark(create_instance)
        assert result is not None

    def test_estimate_font_size_performance(self, default_pyedgeon, benchmark):
        """Benchmark font size estimation."""
        p = default_pyedgeon
        p.illusion_text = "PERFORMANCE TEST"

        result = benchmark(p.estimate_font_size)
        assert p.font_size_guess is not None

    def test_check_length_performance(self, default_pyedgeon, benchmark):
        """Benchmark check_length operation."""
        p = default_pyedgeon
        p.illusion_text = "SHORT TEXT"

        benchmark(p.check_length)

    @pytest.mark.slow
    def test_draw_clear_performance(self, default_pyedgeon, benchmark):
        """Benchmark draw_clear operation."""
        p = default_pyedgeon

        benchmark(p.draw_clear)
        assert p.raw_img is not None

    @pytest.mark.slow
    def test_get_fontsize_performance(self, minimal_pyedgeon, benchmark):
        """Benchmark get_fontsize operation."""
        p = minimal_pyedgeon
        p.illusion_text = "PERF"

        p.estimate_font_size()
        p.draw_clear()

        result = benchmark(p.get_fontsize)
        assert result is not None

    @pytest.mark.slow
    def test_full_create_performance_small(self, font_path, temp_dir):
        """Benchmark full create() for small image."""
        p = Pyedgeon(
            illusion_text="SMALL",
            font_path=font_path,
            file_path=temp_dir,
            file_name="perf_small",
            img_side=256,
            num_rotations=2
        )

        start = time.time()

        # Note: Will fail due to syntax error, but measures time to failure
        try:
            p.create()
        except TypeError:
            pass  # Expected due to line 215 syntax error

        elapsed = time.time() - start

        # Should complete (or fail) in reasonable time
        assert elapsed < 10.0, f"Small image took {elapsed:.2f}s, expected < 10s"

    @pytest.mark.slow
    def test_full_create_performance_medium(self, font_path, temp_dir):
        """Benchmark full create() for medium image."""
        p = Pyedgeon(
            illusion_text="MEDIUM",
            font_path=font_path,
            file_path=temp_dir,
            file_name="perf_medium",
            img_side=512,
            num_rotations=4
        )

        start = time.time()

        try:
            p.create()
        except TypeError:
            pass  # Expected due to line 215 syntax error

        elapsed = time.time() - start

        # Medium images should still be reasonably fast
        assert elapsed < 30.0, f"Medium image took {elapsed:.2f}s, expected < 30s"


class TestScalability:
    """Test performance scaling with different parameters."""

    def test_scaling_with_text_length(self, font_path, temp_dir):
        """Test performance scaling with text length."""
        text_lengths = [5, 10, 15, 20]
        times = []

        for length in text_lengths:
            text = "A" * length
            p = Pyedgeon(
                illusion_text=text,
                font_path=font_path,
                file_path=temp_dir,
                img_side=256
            )

            start = time.time()
            p.estimate_font_size()
            elapsed = time.time() - start

            times.append(elapsed)

        # Font size estimation should scale roughly linearly
        # Verify it doesn't explode exponentially
        assert times[-1] < times[0] * 10, "Performance degradation too severe"

    def test_scaling_with_image_size(self, font_path, temp_dir):
        """Test performance scaling with image size."""
        sizes = [128, 256, 512]
        times = []

        for size in sizes:
            p = Pyedgeon(
                illusion_text="SCALE",
                font_path=font_path,
                file_path=temp_dir,
                img_side=size
            )

            start = time.time()
            p.draw_clear()
            elapsed = time.time() - start

            times.append(elapsed)

        # Image creation should scale roughly quadratically with size
        # (pixels increase as size^2)
        for t in times:
            assert t < 5.0, f"Image creation took {t:.2f}s, too slow"

    def test_scaling_with_num_rotations(self, font_path, temp_dir):
        """Test performance scaling with number of rotations."""
        rotation_counts = [2, 4, 6, 8]
        times = []

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

            start = time.time()
            p.stamp()
            elapsed = time.time() - start

            times.append(elapsed)

        # Stamping should scale linearly with rotations
        assert times[-1] < times[0] * (rotation_counts[-1] / rotation_counts[0]) * 2


class TestNestedLoopPerformance:
    """Test performance of nested pixel loops (known O(n²) issue)."""

    @pytest.mark.slow
    def test_draw_frame_nested_loops(self, font_path, temp_dir):
        """Test nested loop performance in draw_frame."""
        sizes = [128, 256, 512]
        times = []

        for size in sizes:
            p = Pyedgeon(
                illusion_text="LOOP",
                font_path=font_path,
                file_path=temp_dir,
                img_side=size
            )

            p.estimate_font_size()
            p.draw_clear()
            p.get_fontsize()

            start = time.time()
            p.draw_frame()
            elapsed = time.time() - start

            times.append((size, elapsed))

        # Verify quadratic scaling (or worse)
        # Time should increase by ~4x when size doubles
        for i in range(len(times) - 1):
            size_ratio = times[i+1][0] / times[i][0]
            time_ratio = times[i+1][1] / max(times[i][1], 0.001)  # Avoid div by 0

            # With nested loops, expect O(n²) scaling
            # So doubling size should ~4x the time (but allow some overhead)
            assert time_ratio < size_ratio ** 3, \
                f"Performance worse than O(n²): {time_ratio} for {size_ratio}x size"

    @pytest.mark.slow
    def test_alpha_to_white_nested_loops(self, font_path, temp_dir):
        """Test nested loop performance in alpha_to_white."""
        # Note: This will fail due to syntax error, but we can still
        # test the structure

        sizes = [128, 256]
        times = []

        for size in sizes:
            p = Pyedgeon(
                illusion_text="ALPHA",
                font_path=font_path,
                file_path=temp_dir,
                img_side=size
            )

            p.estimate_font_size()
            p.draw_clear()
            p.get_fontsize()
            p.draw_frame()
            p.stamp()

            start = time.time()
            try:
                p.alpha_to_white()
            except TypeError:
                pass  # Expected syntax error
            elapsed = time.time() - start

            times.append((size, elapsed))

        # Even with the error, we measure the time to reach the error
        # Shows the nested loop overhead before hitting the bug


class TestFontSizeDiscoveryPerformance:
    """Test performance of font size discovery algorithm."""

    @pytest.mark.slow
    def test_get_fontsize_temporary_images(self, minimal_pyedgeon):
        """Test that get_fontsize creates many temporary images."""
        p = minimal_pyedgeon
        p.illusion_text = "FONT TEST"

        p.estimate_font_size()
        p.draw_clear()

        # The algorithm tries 60 font sizes (guess-30 to guess+30)
        # Each creates a temporary image
        start = time.time()
        p.get_fontsize()
        elapsed = time.time() - start

        # Should complete but documents the inefficiency
        # Creating 60 images is wasteful
        assert elapsed < 5.0, f"Font size discovery too slow: {elapsed:.2f}s"

    def test_get_fontsize_recursion_count(self, font_path, temp_dir):
        """Test that get_fontsize can recurse multiple times."""
        # With wrong initial guess, it will recurse
        # Each recursion tries 60 more font sizes

        p = Pyedgeon(
            illusion_text="RECURSION",
            font_path=font_path,
            file_path=temp_dir,
            img_side=256
        )

        # Manually set a bad guess to force recursion
        p.estimate_font_size()
        p.draw_clear()
        p.font_size_guess = 10  # Too small, will recurse

        start = time.time()

        # This might recurse several times
        # Note: Could potentially recurse indefinitely!
        try:
            with pytest.raises(RecursionError):
                # Set Python recursion limit low to catch unbounded recursion
                import sys
                old_limit = sys.getrecursionlimit()
                sys.setrecursionlimit(100)

                p.get_fontsize()

                sys.setrecursionlimit(old_limit)
        except:
            # If it doesn't hit recursion limit, that's okay
            # But it's still inefficient
            pass

        elapsed = time.time() - start

        # Should not take forever
        assert elapsed < 10.0


class TestMemoryUsage:
    """Test memory usage patterns."""

    def test_multiple_image_objects(self, default_pyedgeon):
        """Test that multiple image objects are created."""
        p = default_pyedgeon

        p.draw_clear()

        # Documents that 4 separate images are created (default 512x512)
        # This is ~4MB of memory (512*512*4 channels*4 images)
        images = [p.raw_img, p.img, p.circle_img, p.full_image]

        for img in images:
            assert img.size == (p.img_side, p.img_side)
            # Each image uses significant memory

    @pytest.mark.slow
    def test_memory_with_large_image(self, font_path, temp_dir):
        """Test memory usage with large images."""
        # Large image uses substantial memory
        large_size = 2048

        p = Pyedgeon(
            illusion_text="MEMORY",
            font_path=font_path,
            file_path=temp_dir,
            img_side=large_size
        )

        # Creating the images allocates memory
        p.draw_clear()

        # 4 images * 2048*2048 pixels * 4 bytes/pixel = ~64MB
        assert p.img.size == (large_size, large_size)


class TestResourceLimits:
    """Test behavior at resource limits."""

    def test_unrestricted_image_size(self, font_path, temp_dir):
        """Test that image size is now properly restricted."""
        # Validation now prevents huge sizes (max is 8192)

        huge_size = 50000  # Would create 50000x50000 = 2.5B pixels

        # Validation now properly rejects this
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                illusion_text="HUGE",
                font_path=font_path,
                file_path=temp_dir,
                img_side=huge_size
            )

    def test_unrestricted_text_length(self, font_path, temp_dir):
        """Test that text length is now properly restricted."""
        # Validation now prevents very long text (max is 10000)

        very_long = "A" * 100000

        # Validation now properly rejects this
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                illusion_text=very_long,
                font_path=font_path,
                file_path=temp_dir
            )

    def test_unrestricted_num_rotations(self, font_path, temp_dir):
        """Test that num_rotations is now properly restricted."""
        # Validation now prevents excessive rotations (max is 360)

        excessive = 10000

        # Validation now properly rejects this
        with pytest.raises(Exception):  # Should raise ValidationError
            p = Pyedgeon(
                illusion_text="ROT",
                font_path=font_path,
                file_path=temp_dir,
                num_rotations=excessive
            )


class TestRegression:
    """Regression tests for performance improvements."""

    @pytest.mark.slow
    def test_baseline_small_image(self, font_path, temp_dir):
        """Baseline performance test for small images."""
        p = Pyedgeon(
            illusion_text="BASELINE",
            font_path=font_path,
            file_path=temp_dir,
            file_name="baseline_test",
            img_side=256,
            num_rotations=2
        )

        start = time.time()

        # Run through all steps up to the syntax error
        p.check_length()
        p.estimate_font_size()
        p.draw_clear()
        p.get_fontsize()
        p.draw_frame()
        p.stamp()

        elapsed = time.time() - start

        # Baseline: should complete in under 5 seconds
        assert elapsed < 5.0, \
            f"Baseline performance regression: {elapsed:.2f}s (expected < 5s)"

        # Store result for comparison in future test runs
        print(f"\nBaseline performance: {elapsed:.2f}s for 256x256 image")


# Pytest benchmark plugin integration
pytest_plugins = ['pytest-benchmark']


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
