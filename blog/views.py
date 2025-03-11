from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.utils import timezone
from datetime import timedelta

from blog.models import Post, Category


class PostListView(ListView):
    model: Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.all().order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = self.get_custom_message()
        return context

    def get_custom_message(
        self,
    ):
        """Return a custom message depending on the view."""
        return "Latest Posts"


class UserPostListView(PostListView):
    def get_custom_message(self, **kwargs):
        user = self.get_user()
        return f"Posts by {user.get_full_name()}"

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get("username"))

    def get_queryset(self):
        user = self.get_user()
        return Post.objects.filter(author=user).order_by("-date_posted")


class CategoryPostListView(PostListView):
    def get_custom_message(self):
        category = self.get_category()
        return f"Posts in {category.name}"

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs.get("slug"))

    def get_queryset(self):
        category = self.get_category()
        return Post.objects.filter(category=category).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context["category"] = category
        return context


class FeaturedPostListView(PostListView):
    def get_custom_message(self):
        return "Featured posts"

    def get_queryset(self):
        return Post.objects.filter(is_featured=True).order_by("-date_posted")


class LatestPostsView(PostListView):
    number_of_days = 7

    def get_custom_message(self):
        return f"Posts from the last {self.number_of_days} days"

    def get_queryset(self):
        time_limit = timezone.now() - timedelta(days=self.number_of_days)
        return Post.objects.filter(date_posted__gte=time_limit).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/blog/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class AboutView(TemplateView):
    template_name = "blog/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_sidebar"] = True
        context["show_socials"] = True
        context["title"] = "About"
        return context
