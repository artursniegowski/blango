# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from blog.models import Tag
from blog.models import Comment


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)
    title = models.TextField(_("title"),max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.TextField(_("summary"),max_length=500)
    content = models.TextField(_("content"),)
    tags = models.ManyToManyField(Tag, related_name="posts")
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title
