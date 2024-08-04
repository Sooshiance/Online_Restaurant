from django.urls import path

from .views import (registerUser,
                    registerVendor,
                    loginUser,
                    logoutUser,
                    myAccount,
                    custDashboard,
                    vendorDashboard,
                    )


app_name = "user"

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('registerVendor/', registerVendor, name='registerVendor'),

    path('', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('myAccount/', myAccount, name='myAccount'),

    path('custDashboard/', custDashboard, name='custDashboard'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),
]
