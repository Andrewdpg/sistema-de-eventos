# from django.db import models
from djongo import models 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('DJANGO_HOST'))
db = client['django_db']
collection = db['users_customuser']

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, identificacion, nombre_usuario, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('_id', identificacion)

        return self.create_user(identificacion, nombre_usuario, password,  **other_fields)

    # TODO: Esto va para despues (ya que no tiene nada que ver con el register o parecidos)
    def create_user(self, identificacion, nombre_usuario, password, **other_fields):
        
        if not identificacion:
            raise ValueError('Debe ingresar un email')

        user = self.model(identificacion=identificacion, nombre_usuario=nombre_usuario, **other_fields)
        user.set_password(password)

        base_user = document_base_user(nombre_usuario, user.password, identificacion, user.is_superuser)
        collection.insert_one(base_user)
        user = collection.find_one({'identificacion': identificacion})
        # en resumen, mirar si puedo guardar la id y crear la instancia del usuario sin problemas
        return user
    

class CustomUser(AbstractBaseUser):
    _id = models.ObjectIdField(primary_key=True)

    identificacion = models.CharField(max_length=15, unique=True)
    nombre_usuario = models.CharField(max_length=36)
    
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'identificacion'
    REQUIRED_FIELDS = ['nombre_usuario']

    objects = CustomAccountManager()

class AuthenticationCodes(models.Model):
    codigo_url = models.CharField(max_length=30, primary_key=True)
    code = models.CharField(max_length=6)
    empleado_id = models.CharField(max_length=15)