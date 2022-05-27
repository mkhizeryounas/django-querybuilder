from django.test import SimpleTestCase
from ..api_response import ok, error, ERROR_CODES
import logging

logger = logging.getLogger(__name__)


class TestApiResponse(SimpleTestCase):
    def test_should_return_http_200_status_code(self):
        """Test ‘ok’ should return a 200 status code"""
        response = ok()
        self.assertEqual(response.status_code, 200)

    def test_should_return_http_400_status_code(self):
        """Test ‘error’ should return a 400 status code"""
        response = error()
        self.assertEqual(response.status_code, 400)

    def test_should_return_passed_error_status_code(self):
        """Test ‘error’ should return a provided error status code"""
        status_code = 429  # Too Many Requests
        response = error(status=status_code)
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data["message"], ERROR_CODES[status_code])
