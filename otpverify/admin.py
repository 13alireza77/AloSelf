from django.contrib import admin
from .models import PhoneOtp


# Register your models here.
class phoneOtpAdmin(admin.ModelAdmin):
    list_filter = ('phone', 'count',)
    search_fields = ('phone', 'count', 'otp')


admin.site.register(PhoneOtp, phoneOtpAdmin)
