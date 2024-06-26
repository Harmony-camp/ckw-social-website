from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response

from .models import User,FriendshipRequest
from .serializers import UserSerializer,FriendshipRequestSerializer
from .forms import SignupForm,ProfileForm

from notification.utils import create_notification

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
        user = form.save()
        user.is_active = False
        user.save()
        # Send verification email

        url = f"{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}"

        send_mail(
            'Please verify your email',
            f'The url for activating your account is:{url}',
            'noreply@ckw.com',
            [user.email],
            fail_silently=False,
        )

    else:
        # print(form.errors.as_data())
        # message = list(form.errors)
        message = form.errors.as_json()
    print(message)

    return Response({'message': message })


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


@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(),many=True)

    return Response(serializer.data)


@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response({'message':'Email already exists'})
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
        serializer = UserSerializer(user)

        return Response({'message':'information updated','user':serializer.data})

@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(data=request.POST,user=user)

    if form.is_valid():
        form.save()
        return Response({'message':'success'})
    else:

        return Response({'message':form.errors.as_json()})


@api_view(['POST'])
def send_friendship_request(request,pk):
   # print('send_request',pk)
   user = User.objects.get(pk=pk)
   # 发出好友请求的用户
  #  print('req?' ,request.user)
   # 收到请求的用户 可能是自身、可能是另一个
  #  print('acc? ',user)
  #  check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
  #  print('check2-------------')
   check = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

   if not check:
      friendrequest = FriendshipRequest.objects.create(created_for=user,created_by=request.user)
      notification = create_notification(request,'new_friendrequest',friendrequest_id=friendrequest.id)
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

    notification = create_notification(request,'accepted_friendrequest',friendrequest_id=friendship_request.id)

    return Response('friendship request updated')
