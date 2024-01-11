# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from blog.models import Tag


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    title = models.TextField(_("title"),max_length=100)
    slug = models.SlugField()
    summary = models.TextField(_("summary"),max_length=500)
    content = models.TextField(_("content"),)
    tags = models.ManyToManyField(Tag, related_name="posts")

    def __str__(self):
        return self.title
