from django.urls import path
from user.api.views.register import RegisterView
from user.api.views.otp_verification import OTPVerificationView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('verify/otp', OTPVerificationView.as_view(), name='otp_verification'),
]
