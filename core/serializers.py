from rest_framework import serializers
from core.models import Area, Disciplina, Carrera, Modalidad, Perfil, Reserva

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'nombre']

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ['id', 'nombre']

class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = ['id', 'nombre']

class ModalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
        fields = ['id', 'nombre']

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'nombre']

class ReservaSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    disciplina = DisciplinaSerializer(read_only=True)
    carrera = CarreraSerializer(read_only=True)
    modalidad = ModalidadSerializer(read_only=True)
    perfil = PerfilSerializer(read_only=True)
    
    area_id = serializers.PrimaryKeyRelatedField(
        queryset=Area.objects.all(), 
        source='area', 
        write_only=True,
        required=False
    )
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.all(), 
        source='disciplina', 
        write_only=True,
        required=False
    )
    carrera_id = serializers.PrimaryKeyRelatedField(
        queryset=Carrera.objects.all(), 
        source='carrera', 
        write_only=True,
        required=False
    )
    modalidad_id = serializers.PrimaryKeyRelatedField(
        queryset=Modalidad.objects.all(), 
        source='modalidad', 
        write_only=True,
        required=False
    )
    perfil_id = serializers.PrimaryKeyRelatedField(
        queryset=Perfil.objects.all(), 
        source='perfil', 
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Reserva
        fields = [
            'id',
            'area', 'area_id',
            'disciplina', 'disciplina_id',
            'carrera', 'carrera_id',
            'modalidad', 'modalidad_id',
            'perfil', 'perfil_id',
            'responsable', 'cedula',
            'fecha_reserva', 'hora_inicio', 'hora_fin',
            'actividad'
        ]