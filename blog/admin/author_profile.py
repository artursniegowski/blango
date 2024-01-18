# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib import admin
from blog.models import AuthorProfile


class AuthorProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuthorProfile, AuthorProfileAdmin)