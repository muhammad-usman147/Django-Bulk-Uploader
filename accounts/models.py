from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must havee an email Address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


from django.contrib.auth import get_user_model


USER = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


