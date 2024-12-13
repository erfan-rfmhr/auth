from rest_framework_simplejwt.views import TokenObtainPairView

from user.api.serializers.jwt_token import OTPJWTSerializer


class OTPVerificationView(TokenObtainPairView):
    serializer_class = OTPJWTSerializer
