from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.utils.timezone import datetime
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from user.models import User, Profile
from user.forms import Register, LoginForm, OTPForm
from user.utils import detectUser, sendToken, passwordResetEmail
from vendor.forms import RegisterVendor

import pyotp


################################# TODO: Check Role #################################


def checkCustomer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def checkVendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


################################# TODO: Check Role #################################


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "")
        return redirect("home")
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = 2
            user.save()

            # TODO: Send OTP token
            request.session["pk"] = user.pk
            sendToken(request, user.phone)

            messages.success(request, "")
            return redirect('user:otpValidation')
        else:
            messages.error(request, "")
            print(form.errors)
            return redirect("user:register")
    else:
        form = Register()
    return render(request, "user/register.html", {'form':form})


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "")
        return redirect("home")
    if request.method == "POST":
        form = Register(request.POST)
        v_form = RegisterVendor(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user = User.objects.create_user(email=email, password=password,first_name=first_name,
                                            last_name=last_name, phone=phone)
            
            user.role = 1
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = Profile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # TODO: Send OTP token
            request.session["pk"] = user.pk
            sendToken(request, user.phone)

            messages.success(request, "")
            return redirect("user:otpValidation")
    else:
        form = Register()
        v_form = RegisterVendor()
    return render(request, "user/registerVendor.html", {'form':form, 'v_form':v_form})


def otpRegisterValidation(request):
    form = OTPForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            otp = form.cleaned_data.get("otp")
            pk = request.session["pk"]
            otp_secret_key = request.session["otp_secret_key"]
            otp_valid_until = request.session["otp_valid_date"]
            
            if otp_secret_key and otp_valid_until:
                valid_until = datetime.fromisoformat(otp_valid_until)
                
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=180)
                    
                    if totp.verify(otp):
                        user = User.objects.get(pk=pk)
                        
                        user.is_active = True
                        
                        user.save()

                        del request.session["otp_secret_key"]
                        del request.session["otp_valid_date"]
                        
                        messages.success(request, '')
                        
                        return redirect('home')
                    
                    else:
                        messages.error(request, '')
                        return redirect('user:otpValidation')
                else:
                    messages.error(request, '')
                    return redirect('user:otpValidation')
            else:
                messages.error(request, '')
                return redirect('user:otpValidation')
            
        else:
            messages.error(request, '')
            return redirect('user:register')
    return render(request, 'user/otp_register.html', {'form':form})


def loginUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "")
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            user = auth.authenticate(request, phone=phone, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, "")

                return redirect("user:myAccount")
            else:
                messages.error(request, "No valid account found!")
                return redirect("user:login")
        else:
            messages.error(request, "provided credentials are not acceptable!")
            return redirect("user:login")
    else:
        form = LoginForm()
    return render(request, "user/login.html", {'form':form})


def logoutUser(request):
    auth.logout(request)
    messages.info(request, "")
    return redirect("home")


def myAccount(request):
    if request.user.is_authenticated:
        user = request.user 
        redirectURL = detectUser(user)
        return redirect(f"user:{redirectURL}")
    else:
        return redirect("user:login")


@user_passes_test(checkCustomer)
def custDashboard(request):
    if request.user.is_authenticated:
        return render(request, "user/custDashboard.html", {'user':request.user})
    else:
        return redirect("user:login")


@user_passes_test(checkVendor)
def vendorDashboard(request):
    if request.user.is_authenticated:
        return render(request, "user/vendorDashboard.html", {'user':request.user})
    else:
        return redirect("user:login")


########################## TODO: Reset Password ##########################


def forgetPasswordEmail(request):
    if request.user.is_authenticated:
        messages.warning(request, '')
        return redirect('home')
    elif request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            passwordResetEmail(request, user)
            messages.success(request, '')
            return redirect('user:login')
        else:
            messages.error(request, '')
            return redirect('user:forget-password-email')
    return render(request, 'user/forget_password.html')


def resetLinkEmail(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        pass
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, '')
        return redirect('user:confirm-reset-email')
    else:
        messages.error(request, '')
        return redirect('user:login')


def confirmResettingEmail(request):
    if request.user.is_authenticated:
        messages.warning(request, '')
        return redirect('home')
    elif request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()

            del request.session['uid']
            
            messages.success(request, '')
            return redirect('user:login')
        else:
            messages.error(request, '')
            return redirect('user:confirm-reset-email')
    return render(request, 'user/confirm_password.html')
