from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone           = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio             = models.TextField(blank=True, max_length=200)
    xp_points       = models.IntegerField(default=0)
    level           = models.IntegerField(default=1)
    study_streak    = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_level_title(self):
        titles = {1:'Rookie Scholar',2:'Study Apprentice',3:'Knowledge Seeker',
                  4:'Academic Knight',5:'Study Champion',6:'Grand Scholar',7:'Legend'}
        return titles.get(self.level, 'Legend')

    def xp_to_next_level(self):
        return self.level * 500
