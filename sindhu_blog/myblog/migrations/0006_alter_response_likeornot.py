# Generated by Django 5.0.1 on 2024-03-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0005_alter_blog_dislikes_alter_blog_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='likeornot',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
