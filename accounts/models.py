from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# --------------------------------------------------
# RESIDENT MODEL
# --------------------------------------------------

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Resident: {self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


# --------------------------------------------------
# MUNICIPAL STAFF MODEL
# --------------------------------------------------

class MunicipalStaff(models.Model):
    LEVEL_CHOICES = [
        ('junior', 'Junior Staff'),
        ('senior', 'Senior Staff'),
        ('supervisor', 'Supervisor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="junior")

    def __str__(self):
        return f"Staff: {self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


# --------------------------------------------------
# ADMIN PROFILE MODEL
# --------------------------------------------------

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_title = models.CharField(max_length=100, default="System Administrator")

    def __str__(self):
        return f"Admin: {self.user.username}"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username


# --------------------------------------------------
# AUTO-CREATE ADMINPROFILE FOR SUPERUSER
# --------------------------------------------------
# This FIXES the error: "User has no adminprofile"
# When you create Django superuser → AdminProfile auto-created!

@receiver(post_save, sender=User)
def create_admin_profile_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        AdminProfile.objects.get_or_create(user=instance)
