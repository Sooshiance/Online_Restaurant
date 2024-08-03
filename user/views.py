from django.shortcuts import render, redirect
from django.contrib import auth, messages

from user.models import User
from user.forms import Register


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
