from django.db import models

class Paises(models.Model):
    """
    Modelo de Paises

    Atributos:
        - codigo (P-Integer): Codigo del pais
        - nombre (Char 20): Nombre del pais
    """

    codigo = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=20
    )


class Departamentos(models.Model):
    """
    Modelo de Departamentos

    Atributos:
        - codigo (P-Integer): Codigo del departamento
        - nombre (Char 20): Nombre del departamento
        - cod_pais (F-Integer): Codigo del pais al que pertenece el departamento
    """

    codigo = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=20
    )

    cod_pais = models.ForeignKey(
        Paises,
        on_delete=models.CASCADE
    )


class Cuidades(models.Model):
    """
    Modelo de Ciudades

    Atributos:
        - codigo (P-Integer): Codigo de la ciudad
        - nombre (Char 20): Nombre de la ciudad
        - cod_dpto (F-Integer): Codigo del departamento al que pertenece la ciudad
    """

    codigo = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=20
    )

    cod_dpto = models.ForeignKey(
        Departamentos,
        on_delete=models.CASCADE
    )


class Sedes(models.Model):
    """
    Modelo de Sedes

    Atributos:
        - codigo (P-Integer): Codigo de la sede
        - nombre (Char 20): Nombre de la sede
        - cod_ciudad (F-Integer): Codigo de la ciudad al que pertenece la sede
    """

    codigo = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=20
    )

    cod_ciudad = models.ForeignKey(
        Cuidades,
        on_delete=models.CASCADE
    )


class Tipos_Empleado(models.Model):
    """
    Modelo de Tipos_Empleado

    Atributos:
        - nombre (Char 20): Nombre del tipo de empleado
    """

    nombre = models.CharField(
        primary_key=True, 
        max_length=20
    )


class Tipos_Contratacion(models.Model):
    """
    Modelo de Tipos_Contratacion
    
    Atributos:
        - nombre (Char 20): Nombre del tipo de contratacion
    """

    nombre = models.CharField(
        primary_key=True, 
        max_length=20
    )


class Empleados(models.Model):
    """
    Modelo de Empleados

    Atributos:
        - identificacion (P-Char 15): Identificacion del empleado
        - nombres (Char 30): Nombres del empleado
        - apellidos (Char 30): Apellidos del empleado
        - email (Char 30): Email del empleado
        - tipo_contratacion (F-Char 20): Tipo de contratacion del empleado
        - tipo_empleado (F-Char 20): Tipo de empleado
        - cod_facultad (F-Integer): Codigo de la facultad al que pertenece el empleado
        - cod_sede (F-Integer): Codigo de la sede al que pertenece el empleado
        - lugar_nacimiento (F-Integer): Codigo de la ciudad de nacimiento del empleado
    """

    identificacion = models.CharField(
        primary_key=True,
        max_length=15
    )

    nombres = models.CharField(
        max_length=30
    )

    apellidos = models.CharField(
        max_length=30
    )

    email = models.CharField(
        max_length=30
    )

    tipo_contratacion = models.ForeignKey(
        Tipos_Contratacion,
        on_delete=models.CASCADE
    )

    tipo_empleado = models.ForeignKey(
        Tipos_Empleado,
        on_delete=models.CASCADE
    )

    cod_facultad = models.ForeignKey(
        'Facultades',
        on_delete=models.CASCADE
    )

    cod_sede = models.ForeignKey(
        Sedes,
        on_delete=models.CASCADE
    )

    lugar_nacimiento = models.ForeignKey(
        Cuidades,
        on_delete=models.CASCADE
    )


class Facultades(models.Model):
    """
    Modelo de Facultades

    Atributos:
        - codigo (P-Integer): Codigo de la facultad
        - nombre (Char 20): Nombre de la facultad
        - ubicacion (Char 15): Ubicacion de la facultad
        - nro_telefono (Char 15): Numero de telefono de la facultad
        - id_decano (F-Char 15): Identificacion del decano de la facultad
    """

    codigo = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=20
    )

    ubicacion = models.CharField(
        max_length=15
    )

    nro_telefono = models.CharField(
        max_length=15
    )

    id_decano = models.ForeignKey(
        'Empleados',
        on_delete=models.CASCADE
    )


class Areas(models.Model):
    """
    Modelo de Areas

    Atributos:
        - codigo (P-Integer): Codigo del area
        - nombre (Char 20): Nombre del area
        - cod_sede (F-Integer): Codigo de la sede al que pertenece el area
        - id_coordinador (F-Integer): Identificacion del coordinador del area
    """

    codigo = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=20
    )

    codigo_facultades = models.ForeignKey(
        Facultades,
        on_delete=models.CASCADE
    )

    id_coordinador = models.ForeignKey(
        Empleados,
        on_delete=models.CASCADE
    )


class Programas(models.Model):
    """
    Modelo de Programas
    
    Atributos:
        - codigo (P-Integer): Codigo del programa
        - nombre (Char 20): Nombre del programa
        - cod_area (F-Integer): Codigo del area al que pertenece el programa
    """
    
    codigo = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=20
    )

    cod_areas = models.ForeignKey(
        Areas,
        on_delete=models.CASCADE
    )