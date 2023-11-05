from rest_framework import generics
from rest_framework.permissions import AllowAny

from auth_app.serializers import UserSerializer
from auth_app.tasks import send_mail_task


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()

        send_mail_task.delay(new_user.email, new_user.name)
