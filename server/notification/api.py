from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def notifications(request):
    # print(request.user)
    received_notifications = request.user.received_notifications.filter(is_read=False)
    # print(received_notifications)
    serializer = NotificationSerializer(received_notifications,many=True)

    return Response(serializer.data)


@api_view(['POST'])
def read_notification(request,pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()

    return Response({'message':'notification read'})