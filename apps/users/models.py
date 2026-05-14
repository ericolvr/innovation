from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra):
        if not mobile:
            raise ValueError('mobile is required')
        user = self.model(mobile=mobile, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password, **extra):
        extra.setdefault('type', User.ADMIN)
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(mobile, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    MANAGER = 2
    TECHNICIAN = 3

    TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (TECHNICIAN, 'Technician'),
    ]

    client = models.ForeignKey(
        'clients.Client', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='users'
    )
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, unique=True)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=MANAGER)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.name} ({self.mobile})'
