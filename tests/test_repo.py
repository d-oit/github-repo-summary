# tests/test.py
import pytest
from github_summary import get_single_updated_repositories

def test_empty_repositories():
    # Example test to check empty repositories result
    assert get_single_updated_repositories("user", "token", 2024) == []
