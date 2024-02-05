from rest_framework import generics, viewsets
from rest_framework.authentication import SessionAuthentication
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.api.filters import PostFilterSet
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

from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.http import Http404

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
    # specifying ordering fields - not neccesary
    ordering_fields = ["published_at", "author", "title", "slug"]
    # for django filter
    # filterset_fields = ["author", "tags"]
    # custom filterset
    filterset_class = PostFilterSet
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            # published only
            queryset = self.queryset.filter(published_at__lte=timezone.now())
        elif self.request.user.is_staff:
            # allow all
            queryset = self.queryset
        else:
            # filter for own or
            queryset = self.queryset.filter(
                Q(published_at__lte=timezone.now()) | Q(author=self.request.user)
            )

        # adding the filtering based on the passed argument
        time_period_name = self.kwargs.get("period_name")
        
        if not time_period_name:
            # no further filtering required
            return queryset

        if time_period_name == "new":
            return queryset.filter(
                published_at__gte=timezone.now() - timedelta(hours=1)
            )
        elif time_period_name == "today":
            return queryset.filter(
                published_at__date=timezone.now().date(),
            )
        elif time_period_name == "week":
            return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
        else:
            raise Http404(
                f"Time period {time_period_name} is not valid, should be "
                f"'new', 'today' or 'week'"
            )


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
        
        # Unless we manually paginate the querysets, they’ll be returned in the prior, non-paginated format.
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    # cache the list of Posts for two minutes, which means overriding the list() view
    # we add the second decororator with varry on headers / Authorization / Cookie
    # bc we have overwritten the get_queryset, the list of Posts now changes with each user, we need to make sure we add the vary_on_headers()
    @method_decorator(cache_page(120))
    @method_decorator(vary_on_headers("Authorization", "Cookie"))
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

        # Unless we manually paginate the querysets, they’ll be returned in the prior, non-paginated format.
        page = self.paginate_queryset(tag.posts)
        if page is not None:
            post_serializer = PostSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(post_serializer.data)

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