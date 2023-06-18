from django.http import JsonResponse

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response

from .models import User,FriendshipRequest
from .serializers import UserSerializer,FriendshipRequestSerializer
from .forms import SignupForm,ProfileForm

import json



@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar':request.user.get_avatar()
})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
      'email':data.get('email'),
      'name':data.get('name'),
      'password1':data.get('password1'),
      'password2':data.get('password2')
    })

    if form.is_valid():
      form.save()
      
      # 发送验证信息至邮箱
    else:
      message = 'error'  
    return JsonResponse({'message': message })


@api_view(['GET'])
def friends(request,pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
       requests = FriendshipRequest.objects.filter(created_for=request.user,status=FriendshipRequest.SENT)
       requests = FriendshipRequestSerializer(requests,many=True)
       requests = requests.data
    
    friends = user.friends.all()

    return Response({
      'user':UserSerializer(user).data,
      'friends':UserSerializer(friends,many=True).data,
      'requests':requests
    })


@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response('Email already exists')
    else:
        # request.FILES or POST 是django集成後的語法糖
        print(request.POST)
        print(request.FILES)

        form = ProfileForm(request.POST,request.FILES,instance=user)
        
        # file = request.data.get('avatar')      
        # user.name = request.data.get('name')
        # user.save()

        if form.is_valid():
            form.save()

        return Response('information updated')


@api_view(['POST'])
def send_friendship_request(request,pk):
   # print('send_request',pk)
   user = User.objects.get(pk=pk)
   print('req ' ,request.user)
   print('acc? ',user)
   check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_for=user)
   check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_for=request.user)
   print(check1)
   print(check2)

   if not check1 or not check2:
      # FriendshipRequest.objects.create(created_for=user,created_by=request.user)
      return Response('friendship request created')
    
   else:
      return Response('request already sent')
   

  


@api_view(['POST'])
def handle_request(request,pk,status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    return Response('friendship request updated')
