from blog.models import Category
from django.utils.text import slugify

for category in Category.objects.all():
    if not category.slug:  # Only update categories without slugs
        category.slug = slugify(category.name)
        category.save()


print("Slugs updated successfully!")
