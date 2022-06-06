from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import signUpForm, AddTask, ProfileForm, UserChangeProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Task, Profile

# Create your views here.


@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user).count()

    search = ''

    if request.method == 'POST':
        search = request.POST.get('search')

    high_priority_tasks = Task.objects.filter(
        priority='High', user=request.user, task_name__icontains=search).order_by('date', 'time')
    medium_priority_tasks = Task.objects.filter(
        priority='Medium', user=request.user, task_name__icontains=search).order_by('date', 'time')
    low_priority_tasks = Task.objects.filter(
        priority='Low', user=request.user, task_name__icontains=search).order_by('date', 'time')
    return render(request, 'base/dashboard.html', {'tasks': tasks,
                                                   'high_priority_tasks': high_priority_tasks,
                                                   'medium_priority_tasks': medium_priority_tasks,
                                                   'low_priority_tasks': low_priority_tasks,
                                                   'no_of_high_priority_tasks': len(high_priority_tasks),
                                                   'no_of_medium_priority_tasks': len(medium_priority_tasks),
                                                   'no_of_low_priority_tasks': len(low_priority_tasks)
                                                   })


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesnot exist')

    return render(request, 'base/login.html')


def signup(request):
    form = signUpForm()

    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered Successfully! Login here.')
            return redirect('login')
        else:
            messages.error(
                request, 'Please fill the deatils correctly.')

    return render(request, 'base/signup.html', {'form': form})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_task(request):
    if request.method == "POST":
        form = AddTask(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Task set successfully!')
            return redirect('home')
        else:
            messages.error(
                request, 'Error occured while processing your request.')

    form = AddTask()

    return render(request, 'base/add_task.html', {'form': form})


@login_required(login_url='login')
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = AddTask(instance=task)

    if request.method == 'POST':
        form = AddTask(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('home')
        else:
            messages.error(
                request, 'Check you data and try again later.')
    return render(request, 'base/update_task.html', {'form': form})


@login_required(login_url='login')
def delete_task(request, pk):
    Task.objects.get(id=pk).delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('home')


@login_required(login_url='login')
def set_done(request, pk):
    task = Task.objects.get(id=pk)
    task.status = 'Done'
    task.save()
    messages.success(request, 'Task status updated successfully!')
    return redirect('home')


@login_required(login_url='login')
def set_pending(request, pk):
    task = Task.objects.get(id=pk)
    task.status = 'Pending'
    task.save()
    messages.success(request, 'Task status updated successfully!')
    return redirect('home')


@login_required(login_url='login')
def add_profile(request):
    form = ProfileForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Profile added successfully!')
            return redirect('profile')
        else:
            messages.error(
                request, 'Error occured while processing. Kindly check your details and try again.')
            messages.warning(
                request, 'Note: The the number must be a valid 10 digit number.')

    return render(request, 'base/add_profile.html', {'form': form})


@login_required(login_url='login')
def user_profile(request):
    user = User.objects.get(username=request.user.username)
    try:
        profile = Profile.objects.get(user=request.user)
    except Exception:
        return redirect('add_profile')

    return render(request, 'base/profile.html', {'user': user, 'profile': profile})


@login_required(login_url='login')
def update_profile(request):
    form1 = UserChangeProfile(instance=request.user)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form1 = UserChangeProfile(request.POST, instance=request.user)
        form2 = ProfileForm(request.POST, request.FILES, instance=profile)
        if all([form1.is_valid(), form2.is_valid()]):
            form1.save()
            form2.save()
            messages.success(request, 'Profile updated successfully!')
            form = ProfileForm(instance=profile)
            return redirect('profile')
        else:
            messages.error(request,
                           'Error occured while processing your request. Kindly check your credentials and try again.')

    form2 = ProfileForm(instance=profile)

    return render(request, 'base/update_profile.html', {'form1': form1, 'form2': form2})


@login_required(login_url='login')
def change_password(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('home')
        else:
            messages.error(
                request, 'Error occured while processing.')

    return render(request, 'base/change_password.html', {'form': form})


@login_required(login_url='login')
def delete_account(request):

    if request.method == 'POST':
        confirmation = request.POST.get('confirmation')
        if confirmation == 'delete account':
            User.objects.get(username=request.user.username).delete()
            messages.success(
                request, 'Your account has been delete successfully! Thanks for using our Web App.')
            return redirect('login')
        else:
            messages.error(
                request, 'Kindly fill the confirmation data correctly.')
            messages.warning(
                request, 'Note: The confirmation data is case sensitive.')

    return render(request, 'base/delete_account.html')


@login_required(login_url='login')
def delete_history(request):
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation')
        if confirmation == 'delete history':
            Task.objects.filter(user=request.user).delete()
            messages.success(
                request, 'Your account history has been delete successfully!.')
            return redirect('home')
        else:
            messages.error(
                request, 'Kindly fill the confirmation data correctly.')
            messages.warning(
                request, 'Note: The confirmation data is case sensitive.')
    return render(request, 'base/delete_history.html')
