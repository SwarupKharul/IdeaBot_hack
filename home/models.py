from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, mob, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        elif not mob:
            raise ValueError('User must have a mobile number')

        user = self.model(
            email=self.normalize_email(email),
            mob = mob,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mob, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            mob=mob,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    mob = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False) 

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mob'] # Email & Password are required by default.

    def __str__(self):             
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
class Idea(models.Model):
    objects = None
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    stack= models.TextField(null=True, default="Not yet processed")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title