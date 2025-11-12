from rest_framework.generics import ListAPIView
from post.models import Post
from post.serializers import PostSerializer
from utils.response import SuccessResponse


class GetListPosts(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related('user').all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data).to_response()
