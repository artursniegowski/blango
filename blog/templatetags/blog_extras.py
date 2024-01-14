from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

User_Model = get_user_model()

register = template.Library()

@register.filter
def author_details(author: User_Model, current_user: User_Model = None):
    if isinstance(author, User_Model):
        if author == current_user:
            return format_html("<strong>me</strong>")

        if author.first_name and author.last_name:
            author_name = f"{author.first_name} {author.last_name}"
        else:
            author_name = f"{author.username}"

        if author.email:
            author_email = author.email
            # prefix = f'<a href="mailto:{escape(author_email)}">'
            prefix = format_html('<a href="mailto:{}">', author_email)
            suffix = format_html("</a>")
        else:
            prefix = suffix = ""
        
        # return mark_safe(f"{prefix}{escape(author_name)}{suffix}")
        return format_html('{}{}{}', prefix, author_name, suffix)
    else:
        return ""



    