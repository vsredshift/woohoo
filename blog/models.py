from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    CASCADE,
    ForeignKey,
    BooleanField,
    SlugField,
    PositiveIntegerField,
    ManyToManyField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(Model):
    name = CharField(max_length=30, unique=True)
    slug = SlugField(unique=True, blank=True)
    order = PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["order"]


class Post(Model):
    title = CharField(max_length=200)
    subtitle = CharField(max_length=256, null=True)
    content = RichTextField()
    date_posted = DateTimeField(default=timezone.now)
    date_updated = DateTimeField(null=True, default=None)
    author = ForeignKey(User, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE, default=1)

    is_featured = BooleanField(default=False)
    views = PositiveIntegerField(default=0)
    saved_by = ManyToManyField(User, related_name="saved_posts", blank=True)
    likes = ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.pk:
            self.date_updated = timezone.now()
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()


class SavedPost(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE)
    saved_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"


class Comment(Model):
    post = ForeignKey(Post, related_name="comments", on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    content = TextField()
    created_at = DateTimeField(default=timezone.now)
    parent_comment = ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=CASCADE
    )

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

    class Meta:
        ordering = ["-created_at"]
