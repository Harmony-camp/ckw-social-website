import uuid

from django.db import models
from django.utils.timesince import timesince
from datetime import datetime
from django.utils.translation import gettext as _
from django.conf import settings

from account.models import User

def timesince_chinese(dt):
      delta = datetime.now() - dt

      if delta.days > 365:
          years = delta.days // 365
          return _("%d年前") % years
      elif delta.days > 30:
          months = delta.days // 30
          return _("%d个月前") % months
      elif delta.days > 0:
        return _("%d天前") % delta.days
      elif delta.seconds > 3600:
        hours = delta.seconds // 3600
        return _("%d小时前") % hours
      elif delta.seconds > 60:
        minutes = delta.seconds // 60
        return _("%d分钟前") % minutes
      else:
        return _("刚刚")

class Like(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_by = models.ForeignKey(User,related_name='likes',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    body = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def created_at_formatted(self):
        return timesince_chinese(self.created_at)

class PostAttachment(models.Model):
     id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
     image = models.ImageField(upload_to='post_attachments') 
     created_by = models.ForeignKey(User,related_name='posts_attachments',on_delete=models.CASCADE)

     def get_image(self):
         if self.image:
            return settings.WEBSITE_URL + self.image.url
         else:
            return ''


class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    body = models.TextField(blank=True,null=True)

    attachments = models.ManyToManyField(PostAttachment,blank=True)

    is_private = models.BooleanField(default=False)

    likes = models.ManyToManyField(Like,blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment,blank=True)
    comments_count = models.IntegerField(default=0)

    reported_by_users = models.ManyToManyField(User,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def created_at_formatted(self):
        return timesince_chinese(self.created_at)

    # def created_at_formatted(self):
    #     return timesince(self.created_at)

class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()
