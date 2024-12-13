from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.api.serializers.phone import PhoneVerificationSerializer
from user.utils import get_registration_url


class RegisterView(APIView):
    serializer_class = PhoneVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        phone = data["phone"]
        registration_url = get_registration_url(phone, request)
        response_data = {"registration_url": registration_url}
        return Response(response_data, status=status.HTTP_200_OK)
