from distutils.log import debug
from re import S
from rest_framework.views import APIView
from ...models import Post
from ..serializers.post_serializer import PostSerializer
from pro_assignment.utils import api_response as response
from ...services import post_service
from pro_assignment.utils.query_filter import convert_query_to_filter
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

import logging
logger = logging.getLogger(__name__)


class PostView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    # The following code is not required as per the requirements, but to keep RMM Level 3 we should paginate the data and return the hyperlinks for the next and previous pages (https://martinfowler.com/articles/richardsonMaturityModel.html)
    def get_queryset(self):
        """Get list of posts

        Returns:
            list: List of posts
        """
        try:
            # Get the query parameters and convert them to filter
            query = self.request.GET.get('query', None)
            logger.debug(f"Query Params: {query}")
            filter = convert_query_to_filter(query)
            return post_service.list(filter)
        except Exception as e:
            logger.exception(e)
            return response.error(data={"detail": str(e)})

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
            status = 200
            post = {}

            # id is always required to run the post method
            if id is None:
                return response.error(data={
                    "id": ["This field is required."]
                }, status=422)
            hasPost = post_service.exists(id)
            if hasPost:
                # Conflict update the existing post
                post_service.update(id, request.data)
                # post = post_service.get(id)
                logger.debug(
                    f"Updated post with id: {id}")
            elif serializer.is_valid():
                # Create a new entry in the database
                # post = post_service.create(serializer.data)
                post_service.create(serializer.data)
                # status = 201
                logger.debug(f"Created post with id: {id}")
            else:
                return response.error(data=serializer.errors, status=422)

            # Disabling the data return as per requirements
            # serializer = PostSerializer(post)
            # return response.ok(serializer.data, status=status)
            return response.ok(post, status=status)
        except Exception as e:
            logger.exception(e)
            return response.error(data={"detail": str(e)})
