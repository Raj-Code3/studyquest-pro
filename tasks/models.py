from django.db import models
from django.contrib.auth.models import User
from subjects.models import Subject

class Task(models.Model):
    PRIORITY = [('Low','Low'),('Medium','Medium'),('High','High'),('Critical','Critical')]
    STATUS   = [('Pending','Pending'),('In Progress','In Progress'),('Completed','Completed')]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    subject     = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date    = models.DateField(null=True, blank=True)
    priority    = models.CharField(max_length=10, choices=PRIORITY, default='Medium')
    status      = models.CharField(max_length=15, choices=STATUS, default='Pending')
    xp_reward   = models.IntegerField(default=50)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
