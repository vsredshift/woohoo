from django.shortcuts import render

posts = [
    {
        "author": "Jack Jackson",
        "title": "Test Post 1",
        "content": "Test Content 1",
        "date_posted": "January 1, 2025",
    },
    {
        "author": "Mary Maryland",
        "title": "Test Post 2",
        "content": "Test Content 2",
        "date_posted": "January 2, 2025",
    },
    {
        "author": "Jack Jackson",
        "title": "Test Post 3",
        "content": "Test Content 3",
        "date_posted": "January 3, 2025",
    },
]


def home(request):
    context = {"posts": posts}
    return render(request, "blog/index.html", context)


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
