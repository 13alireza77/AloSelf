from django.http import JsonResponse
from accounts.models import User
from .models import PhoneOtp


def phone_verify(phone_number=None):
    if phone_number:
        phone = str(phone_number)
        user = User.objects.filter(phone__iexact=phone)
        if user.exists():
            user = user.first()
            otp = PhoneOtp.objects.filter(phone__iexact=phone)
            if otp.exists() and user.is_active:
                otp = otp.first()
                key = otp.generateOTP(True)
                print(key)
                return JsonResponse(
                    {
                        'status': True,
                        'detail': 'otp sent'
                    }
                )
            else:
                return JsonResponse(
                    {
                        'status': False,
                        'detail': 'generate otp not complete'
                    }
                )
        else:
            return JsonResponse(
                {
                    'status': False,
                    'detail': 'user not registered or disabled'
                }
            )
    else:
        return JsonResponse(
            {
                'status': False,
                'detail': 'phone number is not given in post request'
            }
        )


def otp_verify(phone=None, request_otp=None):
    if phone and request_otp:
        phoneotp = PhoneOtp.objects.filter(phone__iexact=phone)
        if phoneotp.exists():
            phoneotp = phoneotp.first()
            otp = phoneotp.otp
            if str(request_otp) == otp and phoneotp.verify:
                phoneotp.verify = False
                phoneotp.save()
                return True, None
            else:
                return False, JsonResponse(
                    {
                        'status': False,
                        'detail': 'otp not matched or not verified'
                    }
                )
        else:
            return False, JsonResponse(
                {
                    'status': False,
                    'detail': 'First request send otp'
                }
            )

    else:
        return False, JsonResponse(
            {
                'status': False,
                'detail': 'phone number or otp is not given in post request'
            }
        )


def register_otp(phone=None):
    PhoneOtp.objects.filter(phone__iexact=phone).delete()
    phone_otp = PhoneOtp.objects.create(phone=phone)
    key = phone_otp.generateOTP(True)
    phone_otp.verify = True
    phone_otp.save()
    print(key)
    return key
