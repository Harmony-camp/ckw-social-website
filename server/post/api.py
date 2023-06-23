from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import User,FriendshipRequest
from account.serializers import UserSerializer

from notification.utils import create_notification

from .models import Post,Like,Comment,Trend
from .serializers import PostSerializer,PostDetailSerializer,CommentSerializer,TrendSerializer
from .forms import PostForm,AttachmentForm

@api_view(['GET'])
def post_list(request):

    # posts = Post.objects.all()
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id) 

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend','')

    if trend:
      #  posts = posts.filter(body__icontains=trend)
      posts = posts.filter(body__icontains='#'+trend).filter(is_private=False)

    serializer = PostSerializer(posts,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def post_detail(request,pk):
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id) 
    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)
    
    return Response(PostDetailSerializer(post).data)


@api_view(['GET'])
def post_list_profile(request,id):
    # user_ids = []
    # for user in request.user.friends.all():
    #     user_ids.append(user.id)
    
    # fix public/private in profile view
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    if not request.user in user.friends.all():
        posts = posts.filter(is_private=False)
    
    # if you're a friend then,see all posts
    # if you're not a friend,then only see public posts

    # print('req_user',request.user)
    # print('user',user)

    posts_serializer = PostSerializer(posts,many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return Response({
      'posts':posts_serializer.data,
      'user':user_serializer.data,
      'can_send_friendship_request':can_send_friendship_request
    })

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST,request.FILES) 
    
    if attachment_form.is_valid():
        print('attachment_form is valid')
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()
    else:
        print(attachment_form.errors)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return Response(serializer.data)
    else:
        return Response('Error occurred!Add something here later!...')

@api_view(['POST'])
def post_like(request,pk):
    post = Post.objects.get(pk=pk)

    # 查看帖子是否已被点赞
    # print(post.likes.filter(created_by=request.user))

    if not post.likes.filter(created_by=request.user):
         like = Like.objects.create(created_by=request.user)
         post = Post.objects.get(pk=pk)
         post.likes_count = post.likes_count + 1
         post.likes.add(like)
         post.save()

         notification = create_notification(request,'post_like',post_id=post.id)

         return Response('like created')
    else:
         return Response('post already liked')


@api_view(['POST'])
def post_create_comment(request,pk):
    comment = Comment.objects.create(body=request.data.get('body'),created_by=request.user)
    
    post = Post.objects.get(pk=pk)
    post.comments_count = post.comments_count + 1
    post.comments.add(comment)
    post.save()

    notification = create_notification(request,'post_comment',post_id=post.id)

    serializer = CommentSerializer(comment)

    return Response(serializer.data)

@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends,many=True)

    return Response(serializer.data)