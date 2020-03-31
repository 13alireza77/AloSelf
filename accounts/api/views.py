from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import authentication
from rest_framework.views import APIView
from .serializers import RegistrationSerializesr, LoginSerializesr, RefreshPhoneSerializesr
from otpverify.functions import register_otp, phone_verify
from django.contrib.auth import login, logout


class Registration_view(APIView):
    def post(self, request):
        serializer = RegistrationSerializesr(data=request.data)
        if serializer.is_valid():
            try:
                account = serializer.register()
            except Exception:
                return JsonResponse({
                    'status': False,
                    'detail': 'user with this input exist'
                })
            phone = account.phone
            key = register_otp(phone=phone)
            if key:
                return JsonResponse({
                    'status': True,
                    'detail': 'user register'
                })
            else:
                return JsonResponse({
                    'status': False,
                    'detail': 'otp not create'
                })
        else:
            return JsonResponse({
                'status': False,
                'detail': 'inputs not valid'
            })


class Login_View(APIView):
    def post(self, request):
        serializer = LoginSerializesr(data=request.data)
        if serializer.is_valid():
            account, jsonres = serializer.login()
            if account is not None:
                login(request, account)
                return JsonResponse({
                    'status': True,
                    'detail': 'user login'
                })
            else:
                return jsonres
        else:
            return JsonResponse({
                'status': False,
                'detail': 'inputs not valid'
            })


class PhoneVerify_View(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if phone:
            jsonres = phone_verify(phone_number=phone)
            return jsonres
        else:
            return JsonResponse({
                'status': False,
                'detail': 'inputs not valid'
            })


class Logout_view(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        return self.logoutUser(request)

    def logoutUser(self, request):
        try:
            logout(request)
        except (AttributeError, ObjectDoesNotExist):
            return JsonResponse({
                'status': False,
                'detail': 'sth went wrong'
            })
        return JsonResponse({
            'status': True,
            'detail': 'logout'
        })


class RefreshPhone_view(APIView):
    def post(self, request):
        serializer = RefreshPhoneSerializesr(data=request.data)
        if serializer.is_valid():
            jsonres = serializer.refresh()
            return jsonres
        else:
            return serializer.error_messages
