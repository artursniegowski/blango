from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from rest_framework.permissions import IsAdminUser

from blog.api.serializers import PostSerializer
from blog.models import Post


class PostList(generics.ListCreateAPIView):
    # override the default authentication classes on a per-view basis
    # authentication_classes = [SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # However IsAdminUser always returns True from has_object_permission(), even if a user isn’t admin! So by using it we’ll give all permissions to everyone.
    # permission_classes = [AuthorModifyOrReadOnly | IsAdminUser]
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
