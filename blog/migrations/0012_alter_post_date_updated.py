# Generated by Django 5.1.6 on 2025-03-12 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_updated',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
