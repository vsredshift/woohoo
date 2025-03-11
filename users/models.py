from django.db.models import Model, OneToOneField, ImageField, CASCADE
from django.contrib.auth.models import User
from PIL import Image


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    image = ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)