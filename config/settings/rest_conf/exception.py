from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import set_rollback


def exception_handler(exc, context):
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, list):
            data = {"detail": {"global_error_messages": exc.detail}}
        elif isinstance(exc.detail, dict):
            data = exc.detail
        else:
            data = {"detail": {"global_error_messages": [exc.detail]}}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, (Http404, ObjectDoesNotExist)):
        data = {"detail": exc.args[0]}
        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        data = {"detail": exc.args[0]}

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
