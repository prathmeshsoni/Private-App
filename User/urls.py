from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('change-password/' , change_password , name='change_passwordd'),
    # path('accounts/login/' , login_attempt , name="login_attempt"),
    # path('logout/', logout , name = 'logout'),

    path('register/' , register_attempt , name="register_attempt"),
    path('token' , token_send , name="token_send"),
    path('verify/<auth_token>' , verify , name="verify"),

    # path('password-reset/' , forget_passward , name="password_resett"),


    # path('password-reset/done/',
    #     auth_views.PasswordResetDoneView.as_view(
    #         template_name='user/password_reset_done.html'
    #     ),
    #     name='password_reset_done'
    # ),

    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html',
            success_url = '/user/password-reset-complete/'
        ),
        name='password_reset_confirmm'
    ),

    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

]


# handler404 = 'User.views.error_404'