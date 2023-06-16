from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.models import User
from account.serializers import UserSerializer

from .models import Post
from .serializers import PostSerializer
from .forms import PostForm

@api_view(['GET'])
def post_list(request):

    # posts = Post.objects.all()
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id) 

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    serializer = PostSerializer(posts,many=True)

    return Response(serializer.data)

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
        return Response('Error occurred!add something here later!...')

