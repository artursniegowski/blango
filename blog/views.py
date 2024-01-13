from django.shortcuts import render
from django.http import HttpRequest, HttpResponse 
from django.utils import timezone
from blog.models import Post

def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(published_at__lte=timezone.now())
    return render(request, 'blog/index.html', {"posts": posts})