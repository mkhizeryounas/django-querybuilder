from django import views
from ..models import Post
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)


def list(filter=Q()):
    """Get all posts

    Returns:
        list: list of all the records
    """
    return Post.objects.filter(filter).all()


def create(post_data):
    """Create a new post

    Args:
        post_data (dict): post data

    Returns:
        bool: success boolean
    """
    return True if Post.objects.create(**post_data) == 1 else False


def exists(id):
    """Check if post exists

    Args:
        id (str): post id

    Returns:
        bool: True if post exists, False otherwise
    """
    return Post.objects.filter(id=id).exists()


def update(id, post_data):
    """Update post

    Args:
        id (str): post id
        post_data (dict): fields to update

    Returns:
        bool: success boolean
    """
    return True if Post.objects.filter(id=id).update(**post_data) == 1 else False
