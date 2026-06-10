from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject
from .forms import SubjectForm

@login_required
def subject_list(request):
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})

@login_required
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user
            s.save()
            messages.success(request, f'📚 Subject "{s.subject_name}" added!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subjects/subject_form.html', {'form': form, 'title': 'Add Subject'})

@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Subject updated!')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subjects/subject_form.html', {'form': form, 'title': 'Edit Subject'})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, '🗑️ Subject deleted.')
        return redirect('subject_list')
    return render(request, 'subjects/confirm_delete.html', {'object': subject, 'type': 'Subject'})
