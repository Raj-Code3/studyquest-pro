from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Task
from .forms import TaskForm
from subjects.models import Subject
from accounts.models import Profile

@login_required
def task_list(request):
    tasks    = Task.objects.filter(user=request.user)
    subjects = Subject.objects.filter(user=request.user)
    q              = request.GET.get('q','')
    subject_filter = request.GET.get('subject','')
    status_filter  = request.GET.get('status','')
    priority_filter= request.GET.get('priority','')
    if q:
        tasks = tasks.filter(Q(title__icontains=q)|Q(description__icontains=q))
    if subject_filter:
        tasks = tasks.filter(subject__id=subject_filter)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    paginator = Paginator(tasks, 10)
    tasks = paginator.get_page(request.GET.get('page'))
    return render(request, 'tasks/task_list.html', {
        'tasks':tasks,'subjects':subjects,'q':q,
        'subject_filter':subject_filter,'status_filter':status_filter,'priority_filter':priority_filter
    })

@login_required
def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'⚡ Task "{task.title}" created!')
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'New Quest'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Task updated!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Quest'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, '🗑️ Task deleted.')
        return redirect('task_list')
    return render(request, 'tasks/confirm_delete.html', {'object': task, 'type': 'Task'})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status != 'Completed':
        task.status = 'Completed'
        task.save()
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.xp_points += task.xp_reward
        if profile.xp_points >= profile.level * 500:
            profile.level += 1
            messages.success(request, f'🎉 LEVEL UP! You are now Level {profile.level}!')
        else:
            messages.success(request, f'⭐ +{task.xp_reward} XP earned! Task completed!')
        profile.save()
    return redirect('task_list')
