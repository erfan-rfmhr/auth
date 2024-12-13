from django.urls import path

from user.api.views.profile import ProfileViewSet
from user.api.views.register import RegisterView
from user.api.views.otp_verification import OTPVerificationView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ProfileViewSet, basename='user')

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('verify/otp', OTPVerificationView.as_view(), name='otp_verification'),
] + router.urls
