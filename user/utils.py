from django.utils.timezone import datetime, timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

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


def passwordResetEmail(request, user):
    from_email = settings.EMAIL_HOST_USER
    current_site = get_current_site(request)
    mail_subject = 'Forget Password Reset Link'
    message = render_to_string('user/verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_mail = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_mail])
    mail.send()
