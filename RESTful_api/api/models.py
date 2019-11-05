from django.db import models

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=30, blank=False)
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False)
    text = models.CharField(max_length=200, blank=False)