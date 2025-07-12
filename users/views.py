from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .models import CustomUser  # Use CustomUser instead of default User
# from django.contrib.auth.models import CustomUser
from django.http import HttpResponseRedirect,HttpResponse
from .models import Profile
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.decorators import login_required


def history(request):
    return render(request, "accounts/history.html") 


def index(request):
    return render(request, "accounts/index.html") 

def profile(request):
    return render(request, "accounts/profile.html") 

# def signup_page(request):
#     return render(request, "accounts/signup.html")


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user exists
        user_obj = CustomUser.objects.filter(email=email).first()

        if not user_obj:
            messages.warning(request, 'Account not found.')
            return redirect('login')  # Use `redirect('login')` instead of `HttpResponseRedirect(request.path_info)`

        # Check email verification (handle missing profile case)
        if hasattr(user_obj, 'profile') and not user_obj.profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return redirect('login')

        # Authenticate user (ensure email-based authentication works)
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('index')

        messages.warning(request, 'Invalid credentials')
        return redirect('login')

    return render(request, 'accounts/login.html')

def signup_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validate password confirmation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/signup.html')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'accounts/signup.html')

        # Create and save the user
        user = CustomUser.objects.create_user(username=name, email=email, password=password)
        user.set_password(password)  # Hash the password
        user.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info) # Redirect to login page

    return render(request, "accounts/signup.html")


# def signup_page(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")

#        # Capture the grade field

#         if CustomUser.objects.filter(email=email).exists():
#             return render(request, 'accounts/signup.html', {'error': 'Email already exists!'})

#         user = CustomUser.objects.create_user(username=name, email=email, password=password)
    
#         user.set_password(password) # Assign grade separately
#         user.save()

#         # # Send confirmation email
#         # send_mail(
#         #     "Registration Successful",
#         #     f"Welcome {name}! Your registration was successful.",
#         #     "noreply@example.com",
#         #     [email],
#         #     fail_silently=False,
#         # )



#         messages.success(request,'An email has been sent to your mail.')
#         return HttpResponseRedirect(request.path_info)



#     return render(request, "accounts/signup.html")

User = get_user_model()

# 🔹 Define Forms Inside views.py

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username",  "grade"]

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image"]

# 🔹 Edit Profile View
@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = ProfileEditForm(request.POST, instance=user)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!") 
            return redirect("/profile/")  # Redirect after saving
        else:
            messages.error(request, "Please correct the errors below.") 
    else:
        user_form = ProfileEditForm(instance=user)
        profile_form = ProfileImageForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"user_form": user_form, "profile_form": profile_form})


def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')




def materials(request):
    return render(request, 'accounts/materials.html')

def tutor(request):
    return render(request, 'accounts/tutor.html')

def activate_email(request, email_token):
    try:
        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid email token')

