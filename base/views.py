from doctest import Example
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import signUpForm, AddTask
from django.contrib import messages
from .models import Task

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
            messages.success(request, 'Task set seccessfully!')
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
