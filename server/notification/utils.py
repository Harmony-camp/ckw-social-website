from .models import Notification
from post.models import Post
from account.models import FriendshipRequest

"""
    body = models.TextField() done_3
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True) done_4
    type_of_notification = models.CharField(max_length=50,choices=CHOICE_TYPE_OF_NOTIFICATION)  done_2
    created_by = models.ForeignKey(User,related_name='created_notifications',on_delete=models.CASCADE) done_1
    created_for = models.ForeignKey(User,related_name='received_notifications',on_delete=models.CASCADE) done_5
"""

# create_notification(request,'postlike','59b6c1cb-5f7f-4396-a635-12dsd4b0sb58c')

def create_notification(request,type_of_notification,post_id=None,friendrequest_id=None):
    created_for = None


    if type_of_notification == 'post_like':
        body = f'{request.user.name} liked one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'post_comment':
        body = f'{request.user.name} commented on one of your posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} sent you a friend request!'

    elif type_of_notification == 'accepted_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} accepted your friend request!'

    elif type_of_notification == 'rejected_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} rejected your friend request!'

    notification = Notification.objects.create(
      body=body,
      created_by = request.user,
      type_of_notification=type_of_notification,
      post_id=post_id,
      created_for=created_for,
    )

    return notification