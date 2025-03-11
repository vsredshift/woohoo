from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    CASCADE,
    ForeignKey,
)
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Category(Model):
    name = CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Post(Model):
    title = CharField(max_length=100)
    content = TextField()
    date_posted = DateTimeField(default=timezone.now)
    author = ForeignKey(User, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE, default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
