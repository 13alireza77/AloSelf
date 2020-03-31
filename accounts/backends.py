from django.contrib.auth.backends import ModelBackend
from rest_framework.response import Response

from .models import User
from otpverify.functions import otp_verify


class CustomerBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        global jsonres
        phone = kwargs['phone']
        otp = kwargs['otp']
        try:
            user = User.objects.get(phone__iexact=phone)
            auth, jsonres = otp_verify(phone=phone, request_otp=otp)
            if auth:
                return user
            else:
                return jsonres
        except User.DoesNotExist:
            return Response({
                'status': False,
                'detail': 'user not register'
            })
        except Exception:
            return jsonres
