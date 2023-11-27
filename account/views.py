from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from orders.models import Order, OrderItem

from .forms import LoginForm, ProfileForm, UserForm, UserRegistrationForm
from .models import Profile


@login_required
def dashboard(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user.id)
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'user': user, 'profile': profile})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'account/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def orders(request):
    user = request.user
    orders = user.orders.filter(user=user.id).values()
    profile = get_object_or_404(Profile, user=user.id)
    context = {'user': user, 'profile': profile, 'orders': orders}
    return render(request, 'account/orders.html', context)