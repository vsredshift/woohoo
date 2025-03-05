from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Welcome to the Woohoo blog</h1>")


def about(request):
    return HttpResponse("<h1>About Woohoo Blog</h1>")