import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "woohoo.settings")
django.setup()

import random
import lorem
from datetime import datetime

from blog.models import Post, Comment
from django.contrib.auth.models import User

posts = Post.objects.all()

for post in posts:
    if not post.subtitle:
        num_sentences = random.randint(1, 3)
        subheading = " ".join(lorem.sentence() for _ in range(num_sentences))
        post.subtitle = subheading
        post.save()


print("Successfully updated subtitles")
