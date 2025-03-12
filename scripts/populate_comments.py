import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "woohoo.settings")
django.setup()

import random
import lorem  
from datetime import datetime

from blog.models import Post, Comment
from django.contrib.auth.models import User

# Step 1: Get users, posts, and comments
users = User.objects.filter(id__range=[2, 9]) 
posts = Post.objects.all()
comments = Comment.objects.all()  
post_ids = list(Post.objects.values_list("id", flat=True))

# Step 2: Populate likes
for user in users:
    # Randomly choose between 3 and 13 posts for this user to like
    post_ids_to_like = random.sample(post_ids, random.randint(3, 13))
    
    for post_id in post_ids_to_like:
        post = Post.objects.get(id=post_id)
        # Ensure the user hasn't already liked this post
        if user not in post.likes.all():
            post.likes.add(user)
            post.save()

# Step 3: Populate comments
for user in users:
    # Randomly choose between 3 and 10 comments for this user to write
    num_comments = random.randint(3, 10)
    # Randomly choose between 3 and 7 posts where the user will comment
    post_ids_for_comments = random.sample(post_ids, random.randint(3, 7))
    
    for _ in range(num_comments):
        # Randomly choose one of the selected posts
        post_id = random.choice(post_ids_for_comments)
        post = Post.objects.get(id=post_id)
        
        # Generate a random number of sentences (between 1 and 3) for the comment
        num_sentences = random.randint(1, 3)
        comment_content = lorem.sentence()  # Start with one sentence
        
        # If more sentences are needed, add them
        for _ in range(num_sentences - 1):
            comment_content += " " + lorem.sentence()
        
        # Create a comment with the generated content
        post.comments.create(user=user, content=comment_content)

# Step 4: Populate replies to comments
for user in users:
    # Randomly choose between 1 and 7 replies for this user to make
    num_replies = random.randint(1, 7)
    # Randomly choose between 1 and 7 posts
    post_ids_for_replies = random.sample(post_ids, random.randint(1, 7))
    
    for _ in range(num_replies):
        # Randomly choose a post and get its comments
        post_id = random.choice(post_ids_for_replies)
        post = Post.objects.get(id=post_id)
        
        # Choose a random comment to reply to
        if post.comments.exists():
            comment = random.choice(post.comments.all())
        
        # Create a reply (ensure a user can't reply to their own comment, for example)
        if comment.user != user:
            reply_content = lorem.sentence()  # Generate a sentence for the reply
            post.comments.create(user=user, content=reply_content, parent_comment=comment)

# Step 5: Set `date_updated` to None on all posts except 33 and 36
Post.objects.exclude(id__in=[33, 36]).update(date_updated=None)

print("Script executed successfully!")
