from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.models import User

from .models import Conversation,ConversationMessage
from .serializers import ConversationSerializer,ConversationMessageSerializer,ConversationDetailSerializer


@api_view(['GET'])
def conversation_list(request):
    conversation = Conversation.objects.filter(users__in=list([request.user]))
    # print(conversation)

    serializer = ConversationSerializer(conversation,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def conversation_detail(request,pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)

    return Response(serializer.data)

@api_view(['GET'])
def conversation_get_or_create(request,user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        # print('exists')
        conversations = conversations.first()
        
    else:
        # print('create')
        conversations = Conversation.objects.create()
        conversations.users.add(user,request.user)
        conversations.save()
    
    serializer = ConversationDetailSerializer(conversations)

    return Response(serializer.data)

@api_view(['POST'])
def conversation_send_message(request,pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
      conversation=conversation,
      body=request.data.get('body'),
      created_by=request.user,
      sent_to=sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return Response(serializer.data)

