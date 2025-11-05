"""
Accounts app views.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from apps.adoptions.selectors import get_user_applications
from .forms import CustomUserCreationForm, UserUpdateForm
from .services import UserService


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('accounts:account')

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserService.login_user(request=request, user=user)
            messages.success(request, f'Welcome to PawHaven, {user.username}!')
            return redirect(next_url or 'accounts:account')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form, 'next': next_url})


@login_required
def account(request):
    """User account dashboard - redirects admins to admin dashboard"""
    # Check if user is admin and redirect to admin dashboard
    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard:home')
    
    # Regular user logic
    recent_applications = get_user_applications(user=request.user)[:3]
    
    context = {
        'recent_applications': recent_applications,
    }
    return render(request, 'accounts/account.html', context)


@login_required
def user_applications(request):
    """View all user's adoption applications"""
    applications = get_user_applications(user=request.user)
    
    context = {
        'applications': applications,
    }
    return render(request, 'accounts/user_applications.html', context)


@login_required
def edit_profile(request):
    """Edit user profile information"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:account')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


def custom_logout(request):
    """Custom logout view to ensure proper redirect"""
    UserService.logout_user(request=request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('pets:home')