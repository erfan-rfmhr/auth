from rest_framework_simplejwt.views import TokenObtainPairView

from user.api.serializers.jwt_token import OTPJWTSerializer
from user.api.throttles import JWTTokenThrottle


class OTPVerificationView(TokenObtainPairView):
    serializer_class = OTPJWTSerializer
