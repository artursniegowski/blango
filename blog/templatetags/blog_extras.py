from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from blog.models import Post 
from django.utils import timezone

User_Model = get_user_model()

register = template.Library()


# custom filters
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


# simple tags - custom tags

# you can give access to the context variables as the tempalte in which it is used 
# @register.simple_tag(takes_context=True)
# def author_details_tag(context):
#     request = context["request"]
#     current_user = request.user
#     post = context["post"]
#     author = post.author

#     if isinstance(author, User_Model):
#         if author == current_user:
#             return format_html("<strong>me</strong>")

#         if author.first_name and author.last_name:
#             author_name = f"{author.first_name} {author.last_name}"
#         else:
#             author_name = f"{author.username}"

#         if author.email:
#             author_email = author.email
#             # prefix = f'<a href="mailto:{escape(author_email)}">'
#             prefix = format_html('<a href="mailto:{}">', author_email)
#             suffix = format_html("</a>")
#         else:
#             prefix = suffix = ""
        
#         # return mark_safe(f"{prefix}{escape(author_name)}{suffix}")
#         return format_html('{}{}{}', prefix, author_name, suffix)
#     else:
#         return ""

# <small>By {% author_details_tag %} on {{ post.published_at|date:"M, d Y" }}</small>


@register.simple_tag
def row(extra_classes: str = ""):
    """simple tag - start a row - Bootstrap syntax"""
    return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
    """simple tag - end a row - Bootstrap syntax"""
    return format_html('</div>')

@register.simple_tag
def col(extra_classes: str = ""):
    """simple tag - start a col - Bootstrap syntax"""
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    """simple tag - end a col - Bootstrap syntax"""
    return format_html('</div>')

# inclusion tags
@register.inclusion_tag("blog/post-list.html")
def recent_posts(post: Post):
    most_recent_posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": most_recent_posts}