from django.db import models
from django.contrib.auth.models import User
from subjects.models import Subject

class Exam(models.Model):
    TYPES = [('Written','Written'),('MCQ','MCQ'),('Practical','Practical'),('Viva','Viva'),('Online','Online')]

    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    subject   = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    exam_name = models.CharField(max_length=200)
    exam_date = models.DateField()
    exam_type = models.CharField(max_length=15, choices=TYPES, default='Written')
    location  = models.CharField(max_length=200, blank=True)
    notes     = models.TextField(blank=True)

    def __str__(self):
        return f"{self.exam_name} – {self.exam_date}"

    class Meta:
        ordering = ['exam_date']
