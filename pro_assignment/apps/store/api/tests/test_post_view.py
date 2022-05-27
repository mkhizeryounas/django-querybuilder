from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import logging
from ...models import Post
import ddt


logger = logging.getLogger(__name__)


@ddt.ddt
class TestPostView(APITestCase):
    """Test the post view"""

    payload = {
        "id": "first-post",
        "title": "My first post",
        "content": "Hello World!",
        "views": 1,
        "timestamp": 1653124119
    }
    url = reverse('posts')

    def setUp(self):
        """Set up test"""
        Post.objects.create(**self.payload)

    def test_should_create_post(self):
        """Test create post"""
        payload = self.payload.copy()
        payload['id'] = 'second-post'
        response = self.client.post(self.url, payload, format='json')
        data_in_db = Post.objects.get(id=payload['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_in_db.title, payload['title'])
        self.assertEqual(data_in_db.content, payload['content'])
        self.assertEqual(data_in_db.views, payload['views'])
        self.assertEqual(data_in_db.timestamp, payload['timestamp'])

    def test_should_return_422_on_empty_body_post(self):
        """Test create post"""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_should_return_422_on_invalid_body_post(self):
        """Test create post"""
        response = self.client.post(
            self.url, {'id': 'random-id'}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_should_update_post(self):
        """Test update post"""
        update_payload = self.payload.copy()
        update_payload['title'] = 'My updated first post'
        response = self.client.post(
            self.url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = Post.objects.count()
        post = Post.objects.get(id=self.payload['id'])
        self.assertEqual(post.title, update_payload['title'])
        self.assertEqual(count, 1)

    def test_should_list_posts(self):
        """Test list posts"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    @ddt.data(
        {
            'query': f'EQUAL(id, "{payload["id"]}")',
            'expected_eq': True
        },
        {
            'query': f'NOT(EQUAL(id, "{payload["id"]}"))',
            'expected_eq': False
        },
    )
    def test_should_filter_posts(self, params):
        """Test filter posts"""
        payload_sencond_post = self.payload.copy()
        payload_sencond_post['id'] = 'second-post'

        # Create two posts
        Post.objects.create(**payload_sencond_post)

        response = self.client.get(
            self.url, {'query': params['query']})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

        if params['expected_eq']:
            self.assertEqual(response.data[0]['id'], self.payload['id'])
        else:
            self.assertNotEqual(response.data[0]['id'], self.payload['id'])

    def test_should_return_400_on_invalid_filter_posts(self):
        """Test filter posts"""
        response = self.client.get(
            self.url, {'query': f'EQUAL(id, "{self.payload["id"]}"))'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
