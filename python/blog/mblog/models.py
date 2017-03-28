from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length = 20)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 30)
    topicId = models.ForeignKey(Topic, on_delete = models.CASCADE)

class Post(models.Model):
    title = models.CharField(max_length = 100)
    date = models.DateTimeField()
    topicId = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    isDeleted = models.BooleanField()

class post_tag(models.Model):
    postId = models.ForeignKey(Post, on_delete = models.CASCADE)
    tagId = models.ForeignKey(Tag, on_delete = models.CASCADE)

class PostDetails(models.Model):
    postId = models.ForeignKey(Post, on_delete = models.CASCADE)
    sequence = models.IntegerField()
    content = models.TextField()

class User(models.Model):
    name = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 100)
    createdDate = models.DateField()
    active = models.IntegerField()

class Comment(models.Model):
    Comment = models.CharField(max_length = 500)
    ownerId = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    postID = models.ForeignKey(Post, on_delete = models.CASCADE)
    isDeleted = models.BooleanField()
    level = models.IntegerField()
    replyId = models.ForeignKey(u'self', on_delete = models.CASCADE)
