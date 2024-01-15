from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse 
from django.utils import timezone
from blog.models import Post
from blog.forms import CommentForm


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(published_at__lte=timezone.now())
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
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})
