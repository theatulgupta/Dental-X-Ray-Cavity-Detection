"""
Test configuration and fixtures
"""
import pytest
import torch
import numpy as np
from pathlib import Path


@pytest.fixture
def sample_image():
    """Create a sample image for testing"""
    return np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)


@pytest.fixture
def sample_tensor():
    """Create a sample tensor for testing"""
    return torch.randn(1, 3, 640, 640)


@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary test data directory"""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def mock_model_path(tmp_path):
    """Create a mock model path"""
    model_path = tmp_path / "test_model.pt"
    return str(model_path)
