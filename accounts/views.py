from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random
from accounts.utils import send_email_async

def register_view(request):
    if request.user.is_authenticated:
        return redirect('advisor:chat')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        AUO = authenticate(request, username=username, password=password) # Authenticate User Object
        if AUO:
            if AUO.is_active:
                login(request, AUO)
                request.session['username'] = username
                messages.success(request, f"Welcome back, {AUO.username}!")
                return redirect('advisor:chat')
            messages.error(request, "Inactive user")
            return redirect('accounts:login')
        messages.error(request, "Invalid username or password. Please try again.")
        return redirect('accounts:login')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('advisor:home')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('accounts:change_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('accounts:change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # keep user logged in

        messages.success(request, "Password changed successfully.")
        return redirect('advisor:chat')

    return render(request, 'accounts/change_password.html')
User = get_user_model()

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Get first user if multiple accounts share the same email
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No account found with this email.")
            return redirect('accounts:forgot_password')

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save OTP + email in session
        request.session['reset_email'] = email
        request.session['reset_otp'] = str(otp)

        # Send OTP
        send_email_async(
            subject='Dharma AI - Password Reset OTP',
            message=f"""
            Jai Shree Ram 🙏🚩,

You are receiving this message from Dharma AI.

I am Subhajit Kar, the creator of this application, ensuring your login and password recovery process remains secure and smooth.

Please use the OTP below to proceed.  

Your OTP for password reset is: {otp}

If you did not request this, feel free to ignore the email.

May divine guidance be with you.

            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        messages.success(request, "OTP sent to your email.")
        return redirect('accounts:reset_password')

    return render(request, 'accounts/forgot_password.html')



def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        session_email = request.session.get('reset_email')
        session_otp = request.session.get('reset_otp')

        if not session_email or not session_otp:
            messages.error(request, "Session expired. Please try again.")
            return redirect('accounts:forgot_password')

        if email != session_email:
            messages.error(request, "Email does not match.")
            return redirect('accounts:reset_password')

        if otp != session_otp:
            messages.error(request, "Invalid OTP.")
            return redirect('accounts:reset_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('accounts:reset_password')

        
        # FIX: Avoid MultipleObjectsReturned
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "User does not exist.")
            return redirect('accounts:forgot_password')

        # Update password
        user.set_password(new_password)
        user.save()

        # Clear session
        request.session.pop('reset_email', None)
        request.session.pop('reset_otp', None)

        messages.success(request, "Password reset successfully. Please login.")
        return redirect('accounts:login')

    email = request.session.get('reset_email', '')
    return render(request, 'accounts/reset_password.html', {'email': email})