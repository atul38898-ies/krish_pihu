import os  # <--- 1. यहाँ os इम्पोर्ट करें
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    headline = models.CharField(max_length=150, blank=True, help_text="e.g. Python Developer")
    bio = models.TextField(max_length=500, blank=True)
    skills = models.CharField(max_length=250, blank=True, help_text="Comma separated e.g. Python, Django, HTML")
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # settings.SITE_URL का उपयोग करें
        profile_url = f"{settings.SITE_URL}/profile/{self.user.username}/"
        
        # QR Code जनरेट करें
        qr_image = qrcode.make(profile_url)
        canvas = Image.new('RGB', (qr_image.pixel_size, qr_image.pixel_size), 'white')
        canvas.paste(qr_image.get_image(), (0, 0))
        
        fname = f'qr_code-{self.user.username}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()

        # डेटा सेव करें
        super().save(*args, **kwargs)

        # 2. यहाँ चेक करें कि फाइल सच में मौजूद है या नहीं, तभी रीसाइज करें
        if self.profile_pic and os.path.exists(self.profile_pic.path):
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)
