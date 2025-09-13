from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form
        form = UserCreationForm()
    else:
        # Process completed form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page
            login(request, new_user)
            messages.success(request, 'تم إنشاء حسابك بنجاح!')
            return redirect('home')
    
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    """Display the user's profile."""
    return render(request, 'users/profile.html')