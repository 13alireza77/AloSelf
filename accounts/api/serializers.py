from rest_framework import serializers
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

from accounts.models import User, Profile
from otpverify.models import PhoneOtp


class RegistrationSerializesr(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^(\+98|0)?9\d{9}$', message="Phone number must enter in this format")
    ida_regex = RegexValidator(regex=r'[0-9]{8}', message="ida must enter in this format")

    ida = serializers.CharField(validators=[ida_regex], max_length=8)
    phone = serializers.CharField(validators=[phone_regex], max_length=13)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    def register(self):
        account = User(
            phone=self.validated_data['phone'],
            ida=self.validated_data['ida'],
            full_name=f"{self.validated_data['first_name']} {self.validated_data['last_name']}"
        )
        account.set_unusable_password()
        account.save()
        profile = Profile.objects.create(user=account)
        profile.slug = account.full_name
        profile.save()
        return account


class LoginSerializesr(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^(\+98|0)?9\d{9}$', message="Phone number must enter in this format")

    otp = serializers.CharField(max_length=6)
    phone = serializers.CharField(validators=[phone_regex], max_length=13)

    def login(self):
        phone = self.validated_data['phone']
        otp = self.validated_data['otp']
        user = authenticate(phone=phone, otp=otp)
        if type(user) is not JsonResponse and user is not None:
            if user.is_active:
                return user, None
            else:
                return None, JsonResponse({
                    'status': False,
                    'detail': 'disabled account'
                })

        else:
            return None, user


class RefreshPhoneSerializesr(serializers.Serializer):
    phone_regex = RegexValidator(regex=r'^(\+98|0)?9\d{9}$', message="Phone number must enter in this format")

    phone = serializers.CharField(validators=[phone_regex], max_length=13)
    new_phone = serializers.CharField(validators=[phone_regex], max_length=13)

    def refresh(self):
        phone = self.validated_data['phone']
        new_phone = self.validated_data['new_phone']
        user = User.objects.filter(phone__iexact=phone)
        if user is not None:
            user = user.first()
            if user.is_active:
                if str(phone) != str(new_phone):
                    phone_otp = PhoneOtp.objects.filter(phone__iexact=phone)
                    if phone_otp.exists():
                        phone_otp = phone_otp.first()
                        phone_otp.phone = new_phone
                        key = phone_otp.generateOTP()
                        phone_otp.save()
                        print(key)
                    else:
                        JsonResponse({
                            'status': False,
                            'detail': 'User not registered'
                        })
                    user.phone = new_phone
                    user.save()
                    return JsonResponse({
                        'status': True,
                        'detail': 'user phone refresh'
                    })
                else:
                    return JsonResponse({
                        'status': False,
                        'detail': 'inputs are same'
                    })
            else:
                return JsonResponse({
                    'status': False,
                    'detail': 'disabled account'
                })

        else:
            return JsonResponse({
                'status': False,
                'detail': 'User not registered'
            })
