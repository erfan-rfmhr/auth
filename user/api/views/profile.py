from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import mixins

from user.api.serializers.user import UserSerializer

User = get_user_model()


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
