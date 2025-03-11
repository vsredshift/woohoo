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
)
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


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
    title = CharField(max_length=100)
    content = TextField()
    date_posted = DateTimeField(default=timezone.now)
    author = ForeignKey(User, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE, default=1)
    is_featured = BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
