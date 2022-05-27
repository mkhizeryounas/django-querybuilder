from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import logging
from ...models import Post


logger = logging.getLogger(__name__)


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

    def test_should_create_post(self):
        """Test create post"""
        response = self.client.post(self.url, self.payload, format='json')
        data_in_db = Post.objects.get(id=self.payload['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_in_db.title, self.payload['title'])
        self.assertEqual(data_in_db.content, self.payload['content'])
        self.assertEqual(data_in_db.views, self.payload['views'])
        self.assertEqual(data_in_db.timestamp, self.payload['timestamp'])

    def test_should_update_post(self):
        """Test update post"""
        update_payload = self.payload.copy()
        update_payload['title'] = 'My updated first post'
        Post.objects.create(**self.payload)
        response = self.client.post(
            self.url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = Post.objects.count()
        post = Post.objects.get(id=self.payload['id'])
        self.assertEqual(post.title, update_payload['title'])
        self.assertEqual(count, 1)

    def test_should_list_posts(self):
        """Test list posts"""
        Post.objects.create(**self.payload)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_should_filter_posts(self):
        """Test filter posts"""
        payload_sencond_post = self.payload.copy()
        payload_sencond_post['id'] = 'second-post'

        # Create two posts
        Post.objects.create(**self.payload)
        Post.objects.create(**payload_sencond_post)

        # should return a post with id "first-post"
        response_first_filter = self.client.get(
            self.url, {'query': f'EQUAL(id, "{self.payload["id"]}")'})
        self.assertEqual(response_first_filter.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_first_filter.data, list)
        self.assertEqual(len(response_first_filter.data), 1)
        self.assertEqual(
            response_first_filter.data[0]['id'], self.payload["id"])

        # should return a post where id is not "first-post"
        response_second_filter = self.client.get(
            self.url, {'query': f'NOT(EQUAL(id, "{self.payload["id"]}"))'})
        self.assertEqual(response_second_filter.status_code,
                         status.HTTP_200_OK)
        self.assertIsInstance(response_second_filter.data, list)
        self.assertEqual(len(response_second_filter.data), 1)
        self.assertNotEqual(
            response_second_filter.data[0]['id'], self.payload["id"])
