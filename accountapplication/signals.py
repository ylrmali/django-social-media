from django.db.models.signals import post_save
from accountapplication.models import User, Profile
from django.dispatch import receiver


''' When the user create an account, profile automaticly will be create '''
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
