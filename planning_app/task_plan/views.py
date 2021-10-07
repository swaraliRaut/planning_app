from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse


@login_required
def index(request):
    if request.method == "POST":
        task_code = request.POST.get('task_code')
        return redirect(reverse('show_task', args= (task_code, )))
    return render(request, "index.html", {})


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('index'))
        else:
            print(form.errors)
    return render(request, 'log_in.html', {'form': form})


@login_required(login_url='/log_in')
def log_out(request):
    logout(request)
    return redirect(reverse('log_in'))


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('log_in'))
        else:
            print(form.errors)
    return render(request, 'sign_up.html', {'form': form})
