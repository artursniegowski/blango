from blango_auth import views
from django.urls import path, include

app_name = "blango_auth"

urlpatterns = [
  # ext: "accounts/"
  path("profile/", views.profile, name="profile"),
]
