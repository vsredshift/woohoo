from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CategoryPostListView,
    FeaturedPostListView,
    LatestPostsView,
    SavedPostsListView,
    toggle_save_post,
    AboutView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("user/<str:username>/", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "category/<slug:slug>/", CategoryPostListView.as_view(), name="category-posts"
    ),
    path("featured-posts/", FeaturedPostListView.as_view(), name="featured-posts"),
    path("latest-posts/", LatestPostsView.as_view(), name="latest-posts"),
    path("saved-posts/", SavedPostsListView.as_view(), name="saved-posts"),
    path("save-post/<int:post_id>/", toggle_save_post, name="toggle-save-post"),
    path("about/", AboutView.as_view(), name="blog-about"),
]
