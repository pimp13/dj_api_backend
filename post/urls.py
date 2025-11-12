from django.urls import path

from post.views import GetListPosts

urlpatterns = [
    path("", GetListPosts.as_view(), name="get_list_posts"),
]
