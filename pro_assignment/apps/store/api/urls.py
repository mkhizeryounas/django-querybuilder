from django.urls import path
from .views.post_view import PostView


urlpatterns = [
    path('', PostView.as_view(), name='posts'),
]
