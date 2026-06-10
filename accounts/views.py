from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile
from subjects.models import Subject
from tasks.models import Task
from exams.models import Exam
from django.utils import timezone


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f'🎉 Welcome to StudyQuest, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'⚡ Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user    = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    subjects   = Subject.objects.filter(user=user)
    all_tasks  = Task.objects.filter(user=user)
    exams      = Exam.objects.filter(user=user).order_by('exam_date')

    today          = timezone.now().date()
    upcoming_exams = exams.filter(exam_date__gte=today)[:5]
    overdue_tasks  = all_tasks.filter(status='Pending', due_date__lt=today)
    recent_tasks   = all_tasks.order_by('-id')[:6]

    completed = all_tasks.filter(status='Completed').count()
    total     = all_tasks.count()
    progress  = int((completed / total * 100)) if total else 0

    # XP progress bar
    xp_pct = int((profile.xp_points % 500) / 500 * 100) if profile.xp_points else 0

    context = {
        'profile':        profile,
        'total_subjects': subjects.count(),
        'total_tasks':    total,
        'completed_tasks':completed,
        'pending_tasks':  all_tasks.filter(status='Pending').count(),
        'inprogress_tasks': all_tasks.filter(status='In Progress').count(),
        'upcoming_exams': upcoming_exams,
        'overdue_tasks':  overdue_tasks,
        'recent_tasks':   recent_tasks,
        'progress':       progress,
        'xp_pct':         xp_pct,
        'today':          today,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name  = form.cleaned_data['last_name']
            request.user.email      = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, '✅ Profile updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    all_tasks = Task.objects.filter(user=request.user)
    stats = {
        'total_tasks':    all_tasks.count(),
        'completed':      all_tasks.filter(status='Completed').count(),
        'total_subjects': Subject.objects.filter(user=request.user).count(),
        'total_exams':    Exam.objects.filter(user=request.user).count(),
    }
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile, 'stats': stats})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '🔐 Password changed!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    return render(request, 'accounts/change_password.html', {'form': form})
