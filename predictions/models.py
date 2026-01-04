from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Match(models.Model):
    SPORT_CHOICES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('tennis', 'Tennis'),
    ]

    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    sport = models.CharField(max_length=20, choices=SPORT_CHOICES, default='football')
    match_date = models.DateTimeField()
    predicted_winner = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    actual_winner = models.CharField(max_length=100, blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

# Aceasta functie se asigura ca orice User are un UserProfile atasat
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()