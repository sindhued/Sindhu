from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    blogname = models.CharField (max_length = 50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs_written')
    created_date = models.DateTimeField(auto_now_add=True)                 # auto_now_add - automatically set to the current date and time when a new instance of the model is created. However, it does not update the value
    modified_date = models.DateTimeField(auto_now=True)                    # auto_now - automatically updated to the current date and time every time the instance is saved to the database. This includes both creation and subsequent updates to the instance.
    likes = models.ManyToManyField(User, related_name='liked_blog', blank=True)        # creates a new table blog_likes that contains id,blog_id,user_id
    dislikes = models.ManyToManyField(User, related_name='disliked_blog', blank=True)  # creates a new table blog_dislikes that contains id,blog_id,user_id

    #To see the name of the Blog and author name in the Admin page
    def __str__(self):
        return self.blogname + ' | Written By : ' + str(self.author)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    comment_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' %(self.blog.blogname, self.user.username)
class Response(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_responses')
    likeornot = models.BooleanField(blank=True, null=True)
    response_date = models.DateTimeField(auto_now=True)


