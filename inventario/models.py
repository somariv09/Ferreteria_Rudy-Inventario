
from django.db import models


class Categoria(models.Model):

    id_categoria = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=100, unique=True)

    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='descripción'
    )

    imagen = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'categoria'
        managed = False

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    id_producto = models.AutoField(primary_key=True)

    codigo_producto = models.CharField(
        max_length=20,
        unique=True
    )

    nombre = models.CharField(max_length=100)

    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    cantidad = models.IntegerField(default=0)

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_minimo = models.IntegerField(default=0)

    imagen = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.DO_NOTHING,
        db_column='id_categoria',
        related_name='productos'
    )

    class Meta:
        db_table = 'producto'
        managed = False

    def __str__(self):
        return self.nombre


class Movimiento(models.Model):

    ENTRADA = 'ENTRADA'
    SALIDA = 'SALIDA'

    TIPOS_MOVIMIENTO = [
        (ENTRADA, 'Entrada'),
        (SALIDA, 'Salida'),
    ]

    id_movimiento = models.AutoField(primary_key=True)

    codigo_movimiento = models.CharField(
        max_length=20,
        unique=True
    )

    tipo_movimiento = models.CharField(
        max_length=7,
        choices=TIPOS_MOVIMIENTO
    )

    cantidad = models.IntegerField()

    fecha = models.DateTimeField(auto_now_add=False)

    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.DO_NOTHING,
        db_column='id_usuario',
        related_name='movimientos'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.DO_NOTHING,
        db_column='id_producto',
        related_name='movimientos'
    )

    class Meta:
        db_table = 'movimiento'
        managed = False

    def __str__(self):
        return self.codigo_movimiento
