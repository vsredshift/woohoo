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


class Post(Model):
    title = CharField(max_length=100)
    content = TextField()
    date_posted = DateTimeField(default=timezone.now)
    author = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    