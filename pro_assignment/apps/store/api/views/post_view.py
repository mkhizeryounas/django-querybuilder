from distutils.log import debug
from rest_framework.views import APIView
from ...models import Post
from ..serializers.post_serializer import PostSerializer
from pro_assignment.utils import api_response as response
from ...services import post_service
from pro_assignment.utils.query_filter import convert_query_to_filter
from django.db.models import Q

import logging
logger = logging.getLogger(__name__)


class PostView(APIView):
    def get(self, request):
        """Get list of posts

        Args:
            request.query_params.query (str): Post search query i.e. AND(NOT(EQUAL(views, 5)), EQUAL(id, "first-post1"))

        Returns:
            list: List of posts
        """
        try:
            logger.debug(f"Query Params: {request.query_params}")
            # Get the query parameters and convert them to filter
            filter = convert_query_to_filter(
                request.query_params.get('query', None)
            )
            posts = post_service.list(filter)
            serializer = PostSerializer(posts, many=True)
            return response.ok(serializer.data)
        except Exception as e:
            logger.exception(e)
            return response.error(data={"detail": str(e)})

    def post(self, request):
        """Create or update a post

        Args:
            request.data (dict): request payload

        Returns:
            dict: created or updated record
        Raises:
            ValidationError: if id is not provided or serializer fails
        """
        try:
            serializer = PostSerializer(data=request.data)
            id = request.data.get('id', None)
            # id is always required to run the post method
            if id is None:
                return response.error(data={
                    "id": ["This field is required."]
                }, status=422)
            hasPost = post_service.exists(id)
            if hasPost:
                # Conflict update the existing post
                post_service.update(id, request.data)
                logger.debug(
                    f"Updated post with id: {id}")
                return response.ok({})
            elif serializer.is_valid():
                # Create a new entry in the database
                post_service.create(serializer.data)
                logger.debug(f"Created post with id: {id}")
                return response.ok({})
            return response.error(data=serializer.errors, status=422)
        except Exception as e:
            logger.exception(e)
            return response.error(data={"detail": str(e)})
