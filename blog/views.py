from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        "author": "Test User1",
        "title": "Blog Post 1",
        "content": "Post Content 1",
        "date_posted": "January 1, 2025",
    },
    {
        "author": "Test User2",
        "title": "Blog Post 2",
        "content": "Post Content 2",
        "date_posted": "January 10, 2025",
    },
    {
        "author": "Test User3",
        "title": "Blog Post 3",
        "content": "Post Content 3",
        "date_posted": "January 20, 2025",
    },
]


def home(request):
    context = {"posts": posts}
    return render(request, "blog/index.html", context)


def about(request):
    return render(request, "blog/about.html")
