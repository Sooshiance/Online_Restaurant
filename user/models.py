from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser, PermissionsMixin

from user.enums import Role


class AllUser(BaseUserManager):
    def create_user(self, phone, email, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('need Email')
        
        if not phone:
            raise ValueError('need Phone')
        
        if not first_name:
            raise ValueError('need Name')
        
        if not last_name:
            raise ValueError('need SurName')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = False        
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = True        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # TODO: Validators
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='ASCII characters')
    numbers      = RegexValidator(r'^[0-9a]*$', message='Numbers')

    # TODO: Fields
    phone        = models.CharField(max_length=11, unique=True, validators=[numbers])
    email        = models.EmailField(max_length=244, unique=True)
    first_name   = models.CharField(max_length=30, null=True, blank=True)
    last_name    = models.CharField(max_length=50, null=True, blank=True)

    # TODO: Roles
    role         = models.CharField(max_length=1, choices=Role.ROLE_CHOICE, default=2, blank=True, null=True)

    # TODO: Status
    is_active    = models.BooleanField(default=False, null=False)
    is_staff     = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    objects = AllUser()

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    @property
    def fullName(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.phone}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    class Meta:
        ordering = ['pk']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    phone       = models.CharField(max_length=11)
    email       = models.EmailField(max_length=244)
    first_name  = models.CharField(max_length=30, null=True, blank=True)
    last_name   = models.CharField(max_length=50, null=True, blank=True)
    pic         = models.ImageField(upload_to='user/profile/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to="user/cover/", blank=True, null=True)
    address_1   = models.CharField(max_length=256, blank=True, null=True)
    address_2   = models.CharField(max_length=256, blank=True, null=True)
    country     = models.CharField(max_length=30, blank=True, null=True)
    city        = models.CharField(max_length=30, blank=True, null=True)
    pin_code    = models.CharField(max_length=6, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    @property
    def fullName(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self) -> str:
        return f"{self.pk} {self.phone}"
    
    class Meta:
        ordering = ['pk']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
