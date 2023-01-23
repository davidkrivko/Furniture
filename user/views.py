from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from user.models import User
from user.serializers import UserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer
