from django.contrib.auth import get_user_model
from django import template

User_Model = get_user_model()

register = template.Library()

@register.filter
def author_details(author: User_Model):
    if isinstance(author, User_Model):
        if author.first_name and author.last_name:
            return f"{author.first_name} {author.last_name}"
        else:
            return f"{author.username}"
    else:
        return ""



    