from django.urls import path

from .views import (registerUser,
                    registerVendor,
                    otpRegisterValidation,
                    loginUser,
                    logoutUser,
                    myAccount,
                    custDashboard,
                    vendorDashboard,
                    forgetPasswordEmail,
                    resetLinkEmail,
                    confirmResettingEmail,
                    )


app_name = "user"

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('registerVendor/', registerVendor, name='registerVendor'),
    
    path('otp/', otpRegisterValidation, name='otpValidation'),

    path('', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('myAccount/', myAccount, name='myAccount'),

    path('custDashboard/', custDashboard, name='custDashboard'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),

    path('forget-password-email/', forgetPasswordEmail, name='forget-password-email'),
    path('reset-link-email/<uidb64>/<token>/', resetLinkEmail, name='reset-link-email'),
    path('confirm-reset-email/', confirmResettingEmail, name='confirm-reset-email'),
]
