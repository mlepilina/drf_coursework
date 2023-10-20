from rest_framework import generics

from auth_app.serializers import UserSerializer
from auth_app.tasks import send_mail_task


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()
        send_mail_task.delay(new_user.email, new_user.name)
