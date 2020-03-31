from django.db import models
from django.core.validators import RegexValidator
import math, random


class PhoneOtp(models.Model):
    phone_regex = RegexValidator(regex=r'^(\+98|0)?9\d{9}$', message="Phone number must enter in this format")
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=False)
    otp = models.CharField(max_length=4, blank=True)
    count = models.PositiveIntegerField(default=0)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone} is sent {self.otp}"

    def generateOTP(self, changeotp=True):
        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        if changeotp:
            self.otp = OTP
            self.count += 1
            self.verify = True
            self.save()
        return OTP
