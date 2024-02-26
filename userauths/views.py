from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from userauths.forms import UserRegisterForm
from userauths.models import Profile, User

def RegisterView(request):
    
    # if request.user.is_authenticated:
    #     messages.warning(request, "You are registered!")
    #     return redirect('core:feed')
    
    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        
        user = authenticate(email=email, password=password)
        login(request, user)
        
        
        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()
        
        messages.success(request, f"Hi {full_name}. You created account successfully.")
        return redirect('core:feed')
    
    context = {
        'form':form
    }
    return render(request, 'userauths/sign-up.html', context)

def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login!")
        return redirect('core:feed')
        
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
    
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.warning(request, "You are logged in!")
                return redirect('core:feed')
            else:
                messages.error(request, "Username or password does not match")
                return redirect('userauths:sign-up')
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('userauths:sign-up')
            
    return HttpResponseRedirect("/userauths/sign-in/")


def LogoutView(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect("userauths:sign-up")
