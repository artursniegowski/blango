from blog import views
from django.urls import path

app_name = "ecommerce"

urlpatterns = [
  # ext: ""
  path("", views.index),
]
