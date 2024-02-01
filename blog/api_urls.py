from django.urls import path

from blog import api_views

urlpatterns = [
    path("posts/", api_views.post_list, name="api_post_list"),
    path("posts/<int:pk>/", api_views.post_detail, name="api_post_detail"),
]