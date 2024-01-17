from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse 
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers, vary_on_cookie
import logging


logger = logging.getLogger(__name__)

# @cache_page(300)
# @vary_on_cookie # @vary_on_headers("Cookie")
def index(request: HttpRequest) -> HttpResponse:
    # from django.http import HttpResponse
    # logger.debug("Index function is called!")
    # return HttpResponse(str(request.user).encode("ascii"))
    # optimizing the queries, so we dont have to make seperate queries for each post
    # we can query right away all the realted ones
    posts = (Post.objects.filter(published_at__lte=timezone.now()).select_related("author"))
    # defering the colums we dotn use, that way we dont fetch the data we dont use
    # posts = (Post.objects.filter(published_at__lte=timezone.now()).select_related("author").defer("created_at", "modified_at"))
    # same as
    # fetich only the columns we use
    # posts = (
    # Post.objects.filter(published_at__lte=timezone.now())
    # .select_related("author")
    # .only("title", "summary", "content", "author", "published_at", "slug")
    # )
    logger.debug("Got %d posts", len(posts))
    return render(request, 'blog/index.html', {"posts": posts})

def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})

def get_ip(request: HttpRequest):
    return HttpResponse(request.META['REMOTE_ADDR'])
