from django.db import models
from django.conf import settings

from user.models import  Profile


User = settings.AUTH_USER_MODEL


class Vendor(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    user_profile   = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
    vendor_name    = models.CharField(max_length = 60)
    vendor_license = models.ImageField(upload_to='vendor/license/')
    is_approved    = models.BooleanField(default=False)
    created_at     = models.DateField(auto_now=False, auto_now_add=True)
    updated_at     = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.user} {self.vendor_name}'
    
    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ['user']
