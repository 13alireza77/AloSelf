from django.urls import path, include
from .views import Registration_view, Login_View, Logout_view, PhoneVerify_View, RefreshPhone_view

app_name = 'accounts'

urlpatterns = [
    path('accounts/register/', Registration_view.as_view(), name='registration'),
    path('accounts/login/', Login_View.as_view(), name='login'),
    path('accounts/logout/', Logout_view.as_view(), name='logout', ),
    path('accounts/phoneVerify/', PhoneVerify_View.as_view(), name='phoneverify'),
    path('accounts/refreshPhone/', RefreshPhone_view.as_view(), name='refreshphone'),
]
