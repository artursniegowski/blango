# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    value = models.TextField(_("value"), max_length=100, unique=True)

    def __str__(self):
        return self.value
