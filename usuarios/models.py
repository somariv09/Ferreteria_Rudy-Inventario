
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):

    def create_user(self, usuario, nombre, password=None):
        if not usuario:
            raise ValueError('El usuario es obligatorio')

        user = self.model(
            usuario=usuario,
            nombre=nombre
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class Usuario(AbstractBaseUser):

    id_usuario = models.AutoField(
        primary_key=True,
        db_column='id_usuario'
    )

    nombre = models.CharField(max_length=100)

    usuario = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    password = models.CharField(
        max_length=255,
        db_column='contraseña'
    )

    # La tabla existente no tiene estas columnas.
    last_login = None

    objects = UsuarioManager()

    #Campo con el que se valida.
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombre']

    @property
    def is_active(self):
        return True

    class Meta:
        db_table = 'usuario'
        managed = False

    def __str__(self):
        return self.nombre

