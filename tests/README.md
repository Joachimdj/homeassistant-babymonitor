# Testing Guide

## Overview

This project includes comprehensive unit tests to ensure code quality and prevent regressions. Tests run automatically before every `git push` to maintain high code standards.

## Quick Start

### 1. Run Tests Manually

```bash
./run_tests.sh
```

This will:
- Create a virtual environment if needed
- Install test dependencies
- Run all tests with coverage reporting
- Generate a coverage report in `htmlcov/`

### 2. Automatic Pre-Push Testing

Tests run automatically before every push. The pre-push hook is already installed at `.git/hooks/pre-push`.

When you run `git push`, tests will run first:
- ✅ If tests pass → Push proceeds
- ❌ If tests fail → Push is blocked

To skip the pre-push check (not recommended):
```bash
git push --no-verify
```

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Shared fixtures
├── test_storage.py          # Storage functionality tests
├── test_camera_tracker.py   # Camera tracking tests
└── test_sensor.py           # Sensor tests
```

## What's Tested

### Storage Tests (`test_storage.py`)
- ✅ Storage initialization
- ✅ Loading existing data
- ✅ Adding activities
- ✅ Filtering by type
- ✅ Daily activity filtering
- ✅ Activity ordering (newest first)

### Camera Tracker Tests (`test_camera_tracker.py`)
- ✅ Tracker initialization
- ✅ Crying detection (start/end)
- ✅ Duration calculation
- ✅ State change handling
- ✅ Error handling (end without start)
- ✅ Tracker stop/cleanup

### Sensor Tests (`test_sensor.py`)
- ✅ Crying episode counter
- ✅ Temperature sensor
- ✅ Last diaper change sensor
- ✅ Sensor state calculations
- ✅ Extra attributes
- ✅ Integration with storage

## Running Specific Tests

Run all tests:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_storage.py
```

Run specific test:
```bash
pytest tests/test_storage.py::TestBabyMonitorStorage::test_async_add_activity
```

Run with verbose output:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=custom_components/babymonitor --cov-report=html
```

## Coverage Report

After running tests, view the HTML coverage report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

Or view in terminal:
```bash
pytest tests/ --cov=custom_components/babymonitor --cov-report=term-missing
```

## Writing New Tests

### Test File Naming
- Test files must start with `test_`
- Test classes must start with `Test`
- Test methods must start with `test_`

### Example Test

```python
"""Tests for my_module.py"""
import pytest
from custom_components.babymonitor.my_module import MyClass

class TestMyClass:
    """Test MyClass."""
    
    @pytest.fixture
    def my_instance(self):
        """Create instance for testing."""
        return MyClass("test_param")
    
    def test_my_method(self, my_instance):
        """Test my_method returns expected value."""
        result = my_instance.my_method()
        assert result == "expected_value"
    
    @pytest.mark.asyncio
    async def test_async_method(self, my_instance):
        """Test async method."""
        result = await my_instance.async_method()
        assert result is True
```

### Using Fixtures

Fixtures are defined in `conftest.py` and available to all tests:

- `mock_hass` - Mock Home Assistant instance
- `mock_storage_save` - Mock storage save
- `mock_storage_load` - Mock storage load

Example:
```python
def test_with_fixture(self, mock_hass):
    """Test using mock_hass fixture."""
    assert mock_hass.data == {}
```

## Mocking

Use `unittest.mock` for mocking:

```python
from unittest.mock import MagicMock, AsyncMock, patch

# Mock a method
storage = MagicMock()
storage.async_add_activity = AsyncMock()

# Mock with patch
with patch("module.function") as mock_func:
    mock_func.return_value = "mocked"
    result = function_under_test()
```

## Debugging Tests

Run with print statements visible:
```bash
pytest tests/ -s
```

Run with pdb debugger on failure:
```bash
pytest tests/ --pdb
```

Stop at first failure:
```bash
pytest tests/ -x
```

## CI/CD Integration

To integrate with GitHub Actions, create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest tests/ --cov=custom_components/babymonitor
```

## Troubleshooting

### Tests fail with import errors
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-dev.txt
```

### Pre-push hook not running
```bash
# Make hook executable
chmod +x .git/hooks/pre-push

# Verify it exists
ls -la .git/hooks/pre-push
```

### Tests pass locally but fail in hook
```bash
# Run tests the same way the hook does
./run_tests.sh

# Check virtual environment
which python
```

### Need to push despite failing tests
```bash
# Skip pre-push hook (use sparingly!)
git push --no-verify
```

## Best Practices

1. ✅ **Write tests for new features** - Every new feature should have tests
2. ✅ **Test edge cases** - Test boundary conditions and error states
3. ✅ **Keep tests fast** - Mock external dependencies
4. ✅ **One assertion per test** - Makes failures easier to diagnose
5. ✅ **Use descriptive names** - Test names should describe what they test
6. ✅ **Run tests before committing** - Catch issues early
7. ✅ **Maintain high coverage** - Aim for >80% code coverage

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Home Assistant testing guide](https://developers.home-assistant.io/docs/development_testing)

## Getting Help

If you encounter issues with tests:
1. Check the test output for specific error messages
2. Review this guide for common solutions
3. Check existing tests for examples
4. Open an issue on GitHub with test output

---

**Happy testing! 🧪**
