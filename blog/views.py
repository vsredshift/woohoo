from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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

from blog.forms import CommentForm
from blog.models import Comment, Post, Category, SavedPost


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


class MostViewedPostsView(PostListView):
    def get_custom_message(self):
        return f"Most viewed posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-views")[:10]


class MostLikedPostsView(PostListView):
    def get_custom_message(self):
        return f"Most liked posts"

    def get_queryset(self):
        return Post.objects.all().order_by("-likes")[:10]


class SavedPostsListView(LoginRequiredMixin, PostListView):
    def get_queryset(self):
        return super().get_queryset().filter(saved_by=self.request.user)

    def get_custom_message(self):
        return f"Your Saved Posts"


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views += 1  # Increment view count
        post.save(update_fields=["views"])  # Save only the views field
        return post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "subtitle", "header_image", "category", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "subtitle", "header_image", "category", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.date_updated = timezone.now()
        post.save()
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


@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if SavedPost.objects.filter(user=request.user, post=post).exists():
        messages.info(request, "You have already saved this post.")
    else:
        SavedPost.objects.create(user=request.user, post=post)
        messages.success(request, "Post saved to your reading list.")

    return redirect("post-detail", post_id=post.id)


@login_required
def toggle_save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.saved_by.all():
        post.saved_by.remove(request.user)
        messages.info(request, "Removed from saved posts.")
    else:
        post.saved_by.add(request.user)
        messages.success(request, "Post saved successfully!")

    return redirect(request.META.get("HTTP_REFERER", "blog-home"))


@login_required
def toggle_like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("post-detail", pk=post.pk)


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Increment the view count on every request (to simulate post views)
    post.views += 1
    post.save(update_fields=["views"])

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post

            # Check if the comment is a reply
            parent_comment_id = request.POST.get("parent_comment")
            if parent_comment_id:
                new_comment.parent_comment = Comment.objects.get(id=parent_comment_id)

            new_comment.save()
            return redirect("post-detail", pk=post.pk)
    else:
        form = CommentForm()

    # Get all top-level comments (parent_comment is null)
    comments = post.comments.filter(parent_comment__isnull=True)
    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }
    return render(request, "blog/post_detail.html", context)
