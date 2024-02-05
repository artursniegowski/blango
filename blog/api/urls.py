from rest_framework.authtoken import views
from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os
from blog.api.views import PostViewSet, UserDetail, TagViewSet
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="Blango API",
        default_version="v1",
        description="API for Blango Blog",
    ),
    url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio.io/api/v1/",
    public=True,
)

# routers for the viewsets
router = DefaultRouter()
router.register("tags", TagViewSet)
# registering another viewset on the router
router.register("posts", PostViewSet)


urlpatterns = [
    # they will be replaces by the viewsets
    # path("posts/", PostList.as_view(), name="api_post_list"),
    # path("posts/<int:pk>", PostDetail.as_view(), name="api_post_detail"),
    path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)


urlpatterns += [
    path("auth/", include("rest_framework.urls")),
    path("token-auth/", views.obtain_auth_token),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # routers urls for the viewsets
    path("", include(router.urls)),
    # for the filtering
    path(
        "posts/by-time/<str:period_name>/",
        PostViewSet.as_view({"get": "list"}),
        name="posts-by-time",
    ),
]