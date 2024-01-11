# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib import admin
from blog.models import Tag


class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
