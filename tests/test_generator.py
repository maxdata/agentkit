"""Tests for the generator module."""

import pytest
from src.generator import slugify


def test_slugify():
    """Test slugify function."""
    assert slugify("Hello World") == "hello-world"
    assert slugify("A Weather Tool") == "a-weather-tool"
    assert slugify("test!@#$%") == "test"


def test_slugify_max_length():
    """Test slugify respects max length."""
    long_text = "this is a very long description that should be truncated"
    result = slugify(long_text)
    assert len(result) <= 50
