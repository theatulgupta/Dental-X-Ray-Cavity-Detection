"""
Example test file - replace with actual tests for your project
"""
import pytest
import numpy as np


class TestDataPreparation:
    """Tests for data preparation utilities"""

    def test_image_loading(self, sample_image):
        """Test image loading"""
        assert sample_image is not None
        assert sample_image.shape == (640, 640, 3)
        assert sample_image.dtype == np.uint8

    def test_data_directory_creation(self, test_data_dir):
        """Test data directory creation"""
        assert test_data_dir.exists()
        assert test_data_dir.is_dir()


class TestModelInference:
    """Tests for model inference"""

    @pytest.mark.slow
    def test_model_inference_placeholder(self):
        """Placeholder test for model inference"""
        # TODO: Implement actual model inference tests
        assert True


class TestUtilities:
    """Tests for utility functions"""

    def test_basic_math(self):
        """Example basic test"""
        assert 1 + 1 == 2

    @pytest.mark.parametrize("input_val,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_parametrized(self, input_val, expected):
        """Example parametrized test"""
        assert input_val * 2 == expected
