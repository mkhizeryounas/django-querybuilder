from django.test import TestCase
from ..services import post_service
from ..models import Post
from django.db.models import Q


class TestApiResponse(TestCase):

    payload = {
        "id": "first-post",
        "title": "My first post",
        "content": "Hello World!",
        "views": 1,
        "timestamp": 1653124119
    }

    @classmethod
    def setUp(self):
        Post.objects.create(**self.payload)

    def test_should_create_post(self):
        """Test should create a post"""
        payload = self.payload.copy()
        payload['id'] = 'second-post'
        post_service.create(payload)
        self.assertTrue(Post.objects.filter(id=self.payload['id']).exists())

    def test_should_update_post(self):
        """Test should update a post"""
        updated_payload = self.payload.copy()
        updated_payload['views'] = 10
        post_service.update(self.payload['id'], updated_payload)
        post = Post.objects.get(id=self.payload['id'])
        self.assertEqual(post.views, updated_payload['views'])

    def test_should_list_posts(self):
        """Test should list posts"""
        response = post_service.list()
        self.assertEqual(len(response), 1)

    def test_should_filter_posts(self):
        """Test should filter posts"""
        payload_sencond_post = self.payload.copy()
        payload_sencond_post['id'] = 'second-post'

        Post.objects.create(**payload_sencond_post)
        response = post_service.list(Q(id=self.payload['id']))
        self.assertEqual(len(response), 1)

    def test_should_get_post(self):
        """Test should get post"""
        response = post_service.get(self.payload['id'])
        self.assertEqual(response.id, self.payload['id'])
