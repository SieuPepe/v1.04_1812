"""
Pytest configuration and fixtures.

This file contains shared fixtures and configuration for all tests.
"""
import os
import sys
from pathlib import Path
from typing import Generator
import pytest

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "ui: UI tests (slow)")
    config.addinivalue_line("markers", "e2e: End-to-end tests (very slow)")
    config.addinivalue_line("markers", "slow: Tests that take a long time")


# ============================================================================
# Path Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def src_dir(project_root: Path) -> Path:
    """Return the src directory."""
    return project_root / "src"


@pytest.fixture(scope="session")
def tests_dir(project_root: Path) -> Path:
    """Return the tests directory."""
    return project_root / "tests"


@pytest.fixture(scope="session")
def fixtures_dir(tests_dir: Path) -> Path:
    """Return the fixtures directory."""
    return tests_dir / "fixtures"


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_project_data() -> dict:
    """Return sample project data for testing."""
    return {
        "name": "Test Project",
        "code": "TEST-001",
        "budget": 10000.00,
        "currency": "EUR",
        "customer_id": "customer-123",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
    }


@pytest.fixture
def sample_user_data() -> dict:
    """Return sample user data for testing."""
    return {
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "manager",
    }


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_database() -> Generator:
    """
    Provide a mock database for testing.

    Yields:
        Mock database object
    """
    # TODO: Implement mock database
    # For now, return a simple dict to simulate in-memory storage
    db = {
        "projects": {},
        "users": {},
        "parts": {},
    }
    yield db
    # Cleanup after test
    db.clear()


# ============================================================================
# Environment Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def clean_environment() -> Generator:
    """
    Provide a clean environment for each test.

    Saves current env vars and restores them after test.
    """
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture(scope="function", autouse=True)
def reset_test_environment():
    """
    Automatically reset test environment for each test.

    This fixture runs automatically for every test.
    """
    # Setup: Run before each test
    os.environ["TESTING"] = "true"

    yield

    # Teardown: Run after each test
    if "TESTING" in os.environ:
        del os.environ["TESTING"]


# ============================================================================
# UI Testing Fixtures (for future use)
# ============================================================================

@pytest.fixture
def mock_tk_root():
    """
    Provide a mock Tkinter root for UI testing.

    Note: This is a placeholder. Real implementation will need
    actual Tkinter mocking or headless testing setup.
    """
    # TODO: Implement proper Tkinter mocking
    class MockTkRoot:
        def mainloop(self):
            pass

        def destroy(self):
            pass

    return MockTkRoot()


# ============================================================================
# Performance Testing Fixtures
# ============================================================================

@pytest.fixture
def benchmark_timer():
    """
    Provide a simple timer for performance testing.

    Example:
        def test_something(benchmark_timer):
            with benchmark_timer:
                # code to benchmark
                pass
            print(f"Elapsed: {benchmark_timer.elapsed}ms")
    """
    import time

    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.elapsed = None

        def __enter__(self):
            self.start_time = time.perf_counter()
            return self

        def __exit__(self, *args):
            self.end_time = time.perf_counter()
            self.elapsed = (self.end_time - self.start_time) * 1000  # ms

    return Timer()
