# Contributing to Pyedgeon

Thank you for your interest in contributing to Pyedgeon! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Code Guidelines](#code-guidelines)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation Guidelines](#documentation-guidelines)
8. [Pull Request Process](#pull-request-process)
9. [Priority Areas](#priority-areas)
10. [Questions and Support](#questions-and-support)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Prioritize the project's best interests
- Show empathy toward other contributors

### Unacceptable Behavior

- Harassment, discrimination, or trolling
- Publishing others' private information
- Personal attacks or inflammatory comments
- Other conduct that could be considered inappropriate

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git for version control
- Familiarity with PIL/Pillow
- Understanding of optical illusions (helpful but not required)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pyedgeon.git
   cd pyedgeon
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/abehmiel/pyedgeon.git
   ```

## Development Setup

### Install Development Dependencies

```bash
# Install package in development mode
pip install -e .

# Install additional development tools
pip install pytest pytest-cov black flake8 mypy pylint

# Install Pillow (if not already installed)
pip install pillow
```

### Verify Installation

```bash
# Run the demo
python -m pyedgeon.pyedgeon

# Should create "HELLO WORLD.png" in current directory
```

### Keep Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream changes into your main branch
git checkout master
git merge upstream/master
```

## How to Contribute

### Types of Contributions

1. **Bug Fixes** - Fix identified issues
2. **Feature Development** - Add new functionality
3. **Performance Improvements** - Optimize algorithms
4. **Documentation** - Improve docs, add examples
5. **Testing** - Add test coverage
6. **Code Quality** - Refactoring, cleanup

### Contribution Workflow

1. **Check existing issues** - Look for open issues or create a new one
2. **Discuss major changes** - Open an issue to discuss before starting
3. **Create a branch** - Use descriptive branch names
4. **Make changes** - Follow code guidelines
5. **Test thoroughly** - Ensure nothing breaks
6. **Submit PR** - Provide clear description
7. **Address feedback** - Respond to review comments
8. **Merge** - Maintainer will merge when ready

## Code Guidelines

### Style Guide

Follow [PEP 8](https://pep8.org/) - Python Enhancement Proposal 8 (Style Guide for Python Code).

**Key Points**:
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 79 characters for code, 72 for comments
- Use snake_case for functions and variables
- Use PascalCase for class names
- Use UPPER_CASE for constants

### Code Formatting

Use Black for automatic formatting:

```bash
# Format all Python files
black pyedgeon/

# Check without modifying
black --check pyedgeon/
```

### Linting

Run flake8 to check for issues:

```bash
# Check code quality
flake8 pyedgeon/ --max-line-length=88 --extend-ignore=E203,W503

# Common issues to avoid:
# - Unused imports
# - Undefined variables
# - Trailing whitespace
# - Missing docstrings
```

### Type Hints

Add type hints for new code (Python 3.6+):

```python
from typing import Tuple, Optional

def create_image(
    text: str,
    size: int,
    colors: Tuple[int, int, int]
) -> Optional[Image.Image]:
    """Create an image with specified parameters."""
    # ... implementation ...
```

Check types with mypy:

```bash
mypy pyedgeon/ --ignore-missing-imports
```

### Docstrings

Use Google-style docstrings for all public methods:

```python
def method_name(self, param1: str, param2: int) -> bool:
    """Short one-line description.

    Longer description with more details about what this method does,
    how it works, and any important considerations.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is invalid.
        TypeError: When param2 is wrong type.

    Example:
        >>> obj.method_name("test", 42)
        True
    """
```

See `DOCSTRING_EXAMPLES.md` for comprehensive examples.

### Comments

Add comments for complex logic:

```python
# Calculate vertical extent of circle at position x
# using the circle equation: x² + y² = r²
Ysize = 2 * sqrt((self.img_side / 2) ** 2 - (x - (self.img_side / 2)) ** 2)
```

**When to comment**:
- Complex algorithms or math
- Non-obvious design decisions
- Workarounds for specific issues
- Magic numbers (or better: use named constants)

**When not to comment**:
- Obvious operations
- Self-explanatory code
- Redundant information

### Error Handling

Use specific exceptions, avoid bare `except`:

```python
# Bad
try:
    do_something()
except:
    pass

# Good
try:
    do_something()
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise
except PermissionError as e:
    logger.error(f"Permission denied: {e}")
    raise
```

### Security Considerations

When handling file paths or user input:

```python
# Validate paths
from pathlib import Path

def validate_path(user_path: str, base_dir: str) -> Path:
    """Ensure path is within allowed directory."""
    base = Path(base_dir).resolve()
    target = (base / user_path).resolve()

    if not str(target).startswith(str(base)):
        raise ValueError("Path traversal detected")

    return target

# Sanitize filenames
def sanitize_filename(name: str) -> str:
    """Remove dangerous characters from filename."""
    return "".join(c for c in name if c.isalnum() or c in " -_")
```

See `SECURITY.md` for detailed security guidelines.

## Testing Guidelines

### Test Structure

```
tests/
├── __init__.py
├── test_basic.py          # Basic functionality tests
├── test_parameters.py     # Parameter validation tests
├── test_algorithms.py     # Algorithm correctness tests
├── test_integration.py    # End-to-end tests
└── fixtures/              # Test data (fonts, expected outputs)
```

### Writing Tests

Use pytest framework:

```python
import pytest
from pyedgeon import Pyedgeon
from pathlib import Path

def test_basic_creation(tmp_path):
    """Test basic image creation."""
    output = tmp_path / "test.png"

    img = Pyedgeon(
        illusion_text="TEST",
        file_path=str(tmp_path) + "/",
        file_name="test"
    )
    img.create()

    assert output.exists()
    assert output.stat().st_size > 0

def test_invalid_text_length():
    """Test text length validation."""
    img = Pyedgeon(
        illusion_text="A" * 50,
        charmax=10
    )
    img.check_length()

    # Known bug: truncates to 20 instead of charmax
    assert len(img.illusion_text) <= 20

@pytest.mark.parametrize("size", [128, 512, 1024, 2048])
def test_various_sizes(size, tmp_path):
    """Test different image sizes."""
    img = Pyedgeon(
        illusion_text="TEST",
        img_side=size,
        file_path=str(tmp_path) + "/",
        file_name=f"test_{size}"
    )
    img.create()

    output = tmp_path / f"test_{size}.png"
    assert output.exists()
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyedgeon --cov-report=html

# Run specific test file
pytest tests/test_basic.py

# Run specific test
pytest tests/test_basic.py::test_basic_creation

# Run with verbose output
pytest -v
```

### Test Coverage

Aim for:
- **Minimum**: 60% overall coverage
- **Target**: 80% overall coverage
- **Critical paths**: 100% coverage (create pipeline)

### Performance Tests

For performance-sensitive changes:

```python
import time

def test_large_image_performance(tmp_path):
    """Ensure large images complete in reasonable time."""
    start = time.time()

    img = Pyedgeon(
        illusion_text="PERFORMANCE TEST",
        img_side=2048,
        file_path=str(tmp_path) + "/",
        file_name="perf"
    )
    img.create()

    duration = time.time() - start

    # Should complete in under 30 seconds
    assert duration < 30.0
```

## Documentation Guidelines

### What to Document

1. **Public API** - All public classes, methods, parameters
2. **Complex Algorithms** - Mathematical formulas, transformations
3. **Usage Examples** - Common use cases and patterns
4. **Limitations** - Known issues, constraints, edge cases
5. **Security** - Safe usage, validation requirements

### Documentation Files

- **README.md** - User-facing quick start
- **CLAUDE.md** - Comprehensive developer documentation
- **API_REFERENCE.md** - Detailed API documentation
- **SECURITY.md** - Security guidelines
- **CONTRIBUTING.md** - This file
- **DOCSTRING_EXAMPLES.md** - Docstring templates

### Updating Documentation

When making changes:

1. **Update docstrings** - Keep inline documentation current
2. **Update API_REFERENCE.md** - For API changes
3. **Update CLAUDE.md** - For architectural changes
4. **Add examples** - Show usage of new features
5. **Update CHANGELOG** - Document changes (if exists)

### Documentation Style

- **Clear and concise** - Avoid jargon when possible
- **Examples** - Show, don't just tell
- **Consistent terminology** - Use same terms throughout
- **Proper grammar** - Professional writing style
- **Active voice** - "Create an image" not "An image is created"

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No merge conflicts with master
- [ ] Commit messages are clear and descriptive

### PR Title Format

```
[Type] Brief description

Types:
- [BUG] Bug fix
- [FEATURE] New feature
- [PERF] Performance improvement
- [DOCS] Documentation only
- [TEST] Test additions/changes
- [REFACTOR] Code refactoring
- [SECURITY] Security fix
```

Examples:
- `[BUG] Fix syntax error in alpha_to_white method`
- `[FEATURE] Add multi-line text support`
- `[PERF] Vectorize pixel operations with NumPy`

### PR Description Template

```markdown
## Description
Brief description of what this PR does and why.

## Changes
- Bullet point list of changes
- Include modified files/methods
- Note any breaking changes

## Testing
How was this tested?
- Manual testing steps
- New automated tests
- Performance benchmarks (if applicable)

## Related Issues
Fixes #123
Related to #456

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented if necessary)
- [ ] Follows code guidelines
```

### Review Process

1. **Automated checks** - CI runs tests and linting
2. **Maintainer review** - Code review by project maintainer
3. **Address feedback** - Make requested changes
4. **Approval** - Maintainer approves PR
5. **Merge** - Maintainer merges to master

### After Merge

- Delete your feature branch
- Update your fork from upstream
- Close any related issues

## Priority Areas

### Critical (High Priority)

These issues should be addressed first:

1. **Fix syntax error (line 215)**
   ```python
   # Current (broken):
   pixdata[x, y] = self.background_color (255, )

   # Should be:
   pixdata[x, y] = self.background_color + (255, )
   ```

2. **Fix unbounded recursion in get_fontsize()**
   - Add recursion depth limit
   - Replace bare except clause
   - Better error handling

3. **Input validation**
   - Validate file paths
   - Validate numeric parameters
   - Sanitize user input

4. **Security improvements**
   - Path traversal prevention
   - Resource limits
   - File overwrite protection

### Important (Medium Priority)

5. **Add test suite**
   - Basic functionality tests
   - Parameter validation tests
   - Integration tests

6. **Performance optimization**
   - Vectorize pixel operations with NumPy
   - Implement true binary search for font size
   - Reduce temporary image creation

7. **Better error messages**
   - Replace silent failures
   - Clear validation errors
   - Helpful debugging information

8. **API improvements**
   - Return Image object without saving
   - Separate generate() and save() methods
   - Progress callbacks

### Nice to Have (Low Priority)

9. **New features**
   - Multi-line text support
   - Additional distortion geometries
   - Preview mode

10. **Code modernization**
    - Add type hints throughout
    - Use dataclasses for configuration
    - Migrate to setuptools

11. **Documentation**
    - More usage examples
    - Tutorial for beginners
    - Video demonstrations

## Questions and Support

### Getting Help

- **Documentation**: Check CLAUDE.md and API_REFERENCE.md first
- **Issues**: Search existing issues for similar questions
- **New Issue**: Open an issue with [QUESTION] tag
- **Email**: Contact maintainer at abehmiel@gmail.com

### Reporting Bugs

Include in bug reports:
1. **Description** - What happened vs. what you expected
2. **Steps to reproduce** - Minimal code to reproduce the bug
3. **Environment** - Python version, OS, Pillow version
4. **Error messages** - Full stack trace if applicable
5. **Screenshots** - If relevant

### Suggesting Features

Include in feature requests:
1. **Use case** - Why is this feature needed?
2. **Proposed solution** - How should it work?
3. **Alternatives** - Other approaches considered
4. **Examples** - Similar features in other libraries

### Security Issues

**Do not** open public issues for security vulnerabilities.

Email security issues to: abehmiel@gmail.com with subject: [SECURITY] Pyedgeon

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS file (if created)
- Mentioned in release notes for significant contributions
- Credited in commit messages

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Pyedgeon! Your efforts help make optical illusions accessible to everyone.

**Questions?** Open an issue or email abehmiel@gmail.com
