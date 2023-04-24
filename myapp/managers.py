from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, dob, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            **extra_fields
        )

        if password:
            user.password = make_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, dob, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, dob, password, **extra_fields)

