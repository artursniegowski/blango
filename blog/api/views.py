from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.api.serializers import (
    PostSerializer, 
    UserSerializer, 
    PostDetailSerializer,
    TagSerializer,
  )
from blog.models import Post, Tag

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework.exceptions import PermissionDenied

from django.contrib.auth import get_user_model

User = get_user_model()

# class PostList(generics.ListCreateAPIView):
#     # override the default authentication classes on a per-view basis
#     # authentication_classes = [SessionAuthentication]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     # However IsAdminUser always returns True from has_object_permission(), even if a user isn’t admin! So by using it we’ll give all permissions to everyone.
#     # permission_classes = [AuthorModifyOrReadOnly | IsAdminUser]
#     permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer


# replaces the above classes
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer

    # caching /posts/mine   for 5 mins
    # you porbably only want to cache the get all, and get detail request, bc in most casses 
    # ther is no reason to cache views/requests that change something like the put, post, delete ...
    # We also add the caching and vary decorators, so that the response 
    # is cached individually for each user, whether they access by session authentication 
    # (Cookie header) or Authorization header.
    @method_decorator(cache_page(300))
    @method_decorator(vary_on_headers("Authorization"))
    @method_decorator(vary_on_cookie)
    @action(methods=["get"], detail=False, name="Posts by the logged in user")
    def mine(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Posts are yours")
        posts = self.get_queryset().filter(author=request.user)
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    # cache the list of Posts for two minutes, which means overriding the list() view
    @method_decorator(cache_page(120))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)



class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # caching the get request thsi is why we have to define the method here
    @method_decorator(cache_page(300))
    def get(self, *args, **kwargs):
        return super().get(*args, *kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    @action(methods=["get"], detail=True, name="Posts with the Tag")
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request}
        )
        return Response(post_serializer.data)

    # adding both mehtods that we will be caching
    @method_decorator(cache_page(300))
    def list(self, *args, **kwargs):
        return super(TagViewSet, self).list(*args, **kwargs)

    @method_decorator(cache_page(300))
    def retrieve(self, *args, **kwargs):
        return super(TagViewSet, self).retrieve(*args, **kwargs)