# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------


from blog.admin.comment import CommentAdmin
from blog.admin.tag import TagAdmin
from blog.admin.post import PostAdmin
from blog.admin.author_profile import AuthorProfile


__all__ = [
    TagAdmin,
    CommentAdmin,
    PostAdmin,
    AuthorProfile,
]
