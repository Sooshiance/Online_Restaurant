from django.utils.timezone import datetime, timedelta

import pyotp


def sendToken(request, phone):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=180)
    
    otp = totp.now()
    
    request.session["otp_secret_key"] = totp.secret
    
    valid_date = datetime.now() + timedelta(minutes=3)
    
    request.session["otp_valid_date"] = str(valid_date)
    
    print(f"The OTP is : {otp}")


def detectUser(user):
    if user.role == 1:
        redirectUrl = "vendorDashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "custDashboard"
        return redirectUrl
    elif user.superuser == True:
        redirectUrl = "/admin"
        return redirectUrl
