import pytest
from backend.utils.error_mapper import get_user_friendly_error

class TestErrorMapper:
    """Test error message mapping"""
    
    def test_key_error(self):
        """Test KeyError mapping"""
        error = KeyError('amount')
        result = get_user_friendly_error(error)
        assert 'Missing required column' in result
        assert 'amount' in result
    
    def test_unicode_decode_error(self):
        """Test UnicodeDecodeError mapping"""
        error = UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte')
        result = get_user_friendly_error(error)
        assert 'encoding' in result.lower()
        assert 'UTF-8' in result
    
    def test_value_error(self):
        """Test ValueError mapping"""
        error = ValueError('Invalid data format')
        result = get_user_friendly_error(error)
        assert 'Invalid data format' in result
    
    def test_unknown_error(self):
        """Test unknown error defaults"""
        error = RuntimeError('Something went wrong')
        result = get_user_friendly_error(error)
        assert 'unexpected error' in result.lower()
