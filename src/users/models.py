from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    tipo_relacion_c = [
        ('profesor', 'profesor'),
        ('estudiante', 'estudiante'),
        ('graduado', 'graduado'),
        ('empresario', 'empresario'),
        ('administrativo', 'administrativo'),
        ('directivo', 'directivo'),
    ]

    identificacion = models.CharField(max_length=15, unique=True)

    tipo_relacion = models.CharField(choices=tipo_relacion_c, max_length=20) 
    nombre_usuario = models.CharField(max_length=60)
    email = models.EmailField(max_length=30, unique=True)
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ciudad = models.IntegerField()

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'identificacion'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
class AuthenticationCodes(models.Model):
    identificacion = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    codigo = models.CharField(max_length=6, blank=True)