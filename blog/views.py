from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse 
from django.utils import timezone
from blog.models import Post


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, 'blog/index.html', {"posts": posts})

def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {"post": post})