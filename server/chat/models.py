import uuid

from django.db import models
from django.utils.timesince import timesince
from datetime import datetime
from django.utils.translation import gettext as _

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

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    users = models.ManyToManyField(User,related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def modified_at_formatted(self):
        return timesince_chinese(self.created_at)

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    conversation = models.ForeignKey(Conversation,related_name='messages',on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User,related_name='received_messages',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,related_name='sent_messages',on_delete=models.CASCADE)
    
    def created_at_formatted(self):
        return timesince_chinese(self.created_at)

