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
    logging.debug(f"Filter: {filter}")
    return Post.objects.filter(filter).all()


def create(post_data):
    """Create a new post

    Args:
        post_data (dict): post data

    Returns:
        int: success boolean (1 if success, 0 otherwise)
    """
    return Post.objects.update_or_create(**post_data)


def exists(id):
    """Check if post exists

    Args:
        id (str): post id

    Returns:
        bool: True if post exists, False otherwise
    """
    return Post.objects.filter(id=id).exists()


def get(id):
    """Get a single post

    Args:
        id (str): post id

    Returns:
        dict: Single post record
    """
    return Post.objects.filter(id=id).first()


def update(id, post_data):
    """Update post

    Args:
        id (str): post id
        post_data (dict): fields to update

    Returns:
        int: success boolean (1 if success, 0 otherwise)
    """
    return Post.objects.filter(id=id).update(**post_data)
