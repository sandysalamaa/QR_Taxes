from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
    
class User(AbstractBaseUser,PermissionsMixin):
    # Required fields for Firebase
    firebase_uid = models.CharField(max_length=128, unique=True,blank=True , null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # New optional fields
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS= [] # remove the email from the required fields
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
    
    def __str__(self):
        return self.email