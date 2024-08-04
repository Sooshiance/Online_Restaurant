from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from user.models import User, Profile
from user.forms import Register, LoginForm
from user.utils import detectUser
from vendor.forms import RegisterVendor


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
            messages.success(request, "")
            return redirect('home')
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

            messages.success(request, "")
            return redirect("home")
    else:
        form = Register()
        v_form = RegisterVendor()
    return render(request, "user/registerVendor.html", {'form':form, 'v_form':v_form})


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
