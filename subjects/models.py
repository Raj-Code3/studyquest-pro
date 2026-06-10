from django.db import models
from django.contrib.auth.models import User

COLORS = [
    ('#6366f1','Indigo'),('#ec4899','Pink'),('#14b8a6','Teal'),
    ('#f59e0b','Amber'),('#10b981','Green'),('#3b82f6','Blue'),
    ('#ef4444','Red'),('#8b5cf6','Purple'),
]

class Subject(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    subject_name = models.CharField(max_length=200)
    teacher_name = models.CharField(max_length=200, blank=True)
    credits      = models.PositiveIntegerField(default=3)
    description  = models.TextField(blank=True)
    color        = models.CharField(max_length=10, default='#6366f1')
    icon         = models.CharField(max_length=10, default='📚')

    def __str__(self):
        return self.subject_name

    class Meta:
        ordering = ['subject_name']
