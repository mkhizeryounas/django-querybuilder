from django.test import SimpleTestCase
from ..api_response import ok, error, ERROR_CODES
import logging
import ddt

logger = logging.getLogger(__name__)


@ddt.ddt
class TestApiResponse(SimpleTestCase):
    def test_should_return_http_200_status_code(self):
        """Test ‘ok’ should return a 200 status code"""
        response = ok()
        self.assertEqual(response.status_code, 200)

    @ddt.data(
        400, 401, 429
    )
    def test_should_return_http_error_status_code(self, status_code):
        """Test ‘error’ should return a error status code"""
        response = error(status=status_code)
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data.get('message', None),
                         ERROR_CODES[status_code])

    def test_should_return_http_error_default_status_code(self):
        """Test ‘error’ should return a default error status code"""
        response = error(status=411)
        self.assertEqual(response.status_code, 400)
