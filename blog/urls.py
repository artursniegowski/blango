from blog import views
from django.urls import path

app_name = "ecommerce"

urlpatterns = [
  # ext: ""
  path("", views.index, name="posts-index"),
  path("post/<slug>/", views.post_detail, name="blog-post-detail"),
  path("ip/", views.get_ip, name="get-ip"),
  path("post-table/", views.post_table, name="blog-post-table"),
]
