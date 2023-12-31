import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
  def _create_user(self,email,password,**extra_fields):
      if not email:
         raise ValueError("没有提供有效的邮箱地址")

      email = self.normalize_email(email)
      user = self.model(email=email,**extra_fields)
      user.set_password(password)
      user.save(using=self._db)

      return user
  
  def create_user(self,email=None,password=None,**extra_fields):
      extra_fields.setdefault('is_staff',False)
      extra_fields.setdefault('is_superuser',False)
      return self._create_user(email,password,**extra_fields)
  
  def create_superuser(self,email=None,password=None,**extra_fields):
      extra_fields.setdefault('is_staff',True)
      extra_fields.setdefault('is_superuser',True)
      return self._create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255,blank=True,default='')
    avatar = models.ImageField(upload_to='avatars',blank=True,null=True)

    friends = models.ManyToManyField('self')
    friends_count = models.IntegerField(default=0)

    people_you_may_know = models.ManyToManyField('self')

    posts_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_avatar(self):
      if self.avatar:
          return settings.WEBSITE_URL + self.avatar.url
      else:
          return 'https://picsum.photos/200/200'

    # class Meta:
    #     db_table = 'mytable'


class FriendshipRequest(models.Model):
  # 设置请求状态
  SENT = 'sent'
  ACCEPTED = 'accepted'
  REJECTED = 'rejected'

  STATUS_CHOICES = (
    (SENT,'Sent'),
    (ACCEPTED,'Accepted'),
    (REJECTED,'Rejected')
  )

  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  # 为收到发送的好友请求设置一个变量
  created_for = models.ForeignKey(User,related_name='received_friendship_requests',on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User,related_name='created_friendship_requests',on_delete=models.CASCADE)
  status =  models.CharField(max_length=20,choices=STATUS_CHOICES,default=SENT)



