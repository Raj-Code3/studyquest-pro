from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam
from .forms import ExamForm

@login_required
def exam_list(request):
    exams = Exam.objects.filter(user=request.user)
    return render(request, 'exams/exam_list.html', {'exams': exams})

@login_required
def exam_add(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, user=request.user)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.save()
            messages.success(request, f'📅 Exam "{exam.exam_name}" scheduled!')
            return redirect('exam_list')
    else:
        form = ExamForm(user=request.user)
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Schedule Exam'})

@login_required
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Exam updated!')
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam, user=request.user)
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Edit Exam'})

@login_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk, user=request.user)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, '🗑️ Exam deleted.')
        return redirect('exam_list')
    return render(request, 'exams/confirm_delete.html', {'object': exam, 'type': 'Exam'})
