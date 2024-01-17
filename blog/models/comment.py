# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings

# By utilizing ContentType we can allow a model to be related to any number of models by just adding three attributes to a Model:
# A ForeignKey field that points to a ContentType. Normally this is called content_type
# A PositiveIntegerField that stores the primary key of the related object. Normally this is called object_id
# A GenericForeignKey field, a special type of field that will look up the object from the other two new fields.
class Comment(models.Model):
    """model for Comment, can be related to any number of models"""
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
