from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import User
from account.serializers import UserSerializer

from .models import Post,Like,Comment,Trend
from .serializers import PostSerializer,PostDetailSerializer,CommentSerializer,TrendSerializer
from .forms import PostForm

@api_view(['GET'])
def post_list(request):

    # posts = Post.objects.all()
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id) 

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend','')

    if trend:
       posts = posts.filter(body__icontains=trend)

    serializer = PostSerializer(posts,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def post_detail(request,pk):
    post = Post.objects.get(pk=pk)

    
    return Response(PostDetailSerializer(post).data)


@api_view(['GET'])
def post_list_profile(request,id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts,many=True)
    user_serializer = UserSerializer(user)

    return Response({
      'posts':posts_serializer.data,
      'user':user_serializer.data
    })

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
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
         post.like_count = post.likes_count + 1
         post.likes.add(like)
         post.save()

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

    serializer = CommentSerializer(comment)

    return Response(serializer.data)

@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends,many=True)

    return Response(serializer.data)