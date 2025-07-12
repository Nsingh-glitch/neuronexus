from django.db import models
from django.contrib.auth.models import AbstractUser
 # Importing BaseModel
from django.db.models.signals import post_save
# from Base import BaseModel
from django.contrib.auth.models import User
import uuid
from Base.emails import send_account_activation_email
from django.dispatch import receiver
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True) 
    grade = models.CharField(max_length=10, blank=True, null=True)  # Optional field

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles", blank=True, null=True, default="profiles/default-profile.jpg")


    def __str__(self):
        return f"{self.user.email}'s Profile"

# @receiver(post_save,sender=CustomUser)
# def send_email_token(sender,instance,created,**kwargs):
#     try:
#         if created:
#             email_token=str(uuid.uuid4())
#             Profile.objects.create(user=instance, email_token=email_token)
#             email=instance.email
#             send_account_activation_email(email,email_token)
#     except Exception as e:
#         print(e)


@receiver(post_save, sender=CustomUser)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create( user=instance, 
                                    email_token=email_token,
                                     profile_image="profiles/default-profile.jpg" )
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(f"Error sending email: {e}")


