# Generated by Django 5.0.1 on 2024-03-13 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_blog_dislikes_blog_likes_alter_blog_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
