from django.urls import path, include

app_name = 'user'

urlpatterns = [
    path("", include("user.api.urls")),
]
