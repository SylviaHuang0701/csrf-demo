from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegistrationForm

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})
    else:
        return redirect('login')
    
@login_required
def update_profile(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        request.user.email = new_email
        request.user.save()
        request.user.refresh_from_db()
        messages.success(request, '个人信息修改成功')
        referer = request.META.get('HTTP_REFERER', '')
        print(f"Referer: {referer}")
        if referer == 'http://127.0.0.1:8080/':
            # 如果来自恶意网站，返回简单的响应
            return JsonResponse({'status': 'success', 'message': 'Email updated'})
        
        # 如果是正常来源，请重定向到 profile
        return redirect('users:profile')
    return render(request, 'update_profile.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:profile')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # 重定向到登录页面

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # 登录用户
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})
    else:
        return render(request, 'home.html')

@login_required    
def grant_superuser(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.is_superuser = True
            user.is_staff = True
            user.save()
            referer = request.META.get('HTTP_REFERER', '')
            if referer == 'http://127.0.0.1:8080/':
                return JsonResponse({'status': 'success', 'message': 'Superuser status granted'})
            return HttpResponseRedirect(reverse('users:profile'))
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def delete_account(request):
    try:
        user = request.user
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'Account deleted successfully'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'})