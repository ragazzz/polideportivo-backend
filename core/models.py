from django.db import models

class Area(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
    
class Disciplina(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
    
class Carrera(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Modalidad(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
    
class Perfil(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    actividad = models.TextField()
