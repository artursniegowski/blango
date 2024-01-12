# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib import admin
from blog.models import Comment


class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)