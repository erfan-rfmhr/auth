from rest_framework_simplejwt.views import TokenObtainPairView

from user.api.serializers.jwt_token import PasswordJWTSerializer


class PasswordVerificationView(TokenObtainPairView):
    serializer_class = PasswordJWTSerializer
