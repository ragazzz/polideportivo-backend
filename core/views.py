from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.utils import timezone
import pandas as pd
from core.models import Area, Disciplina, Carrera, Modalidad, Perfil, Reserva
from core.serializers import (
    AreaSerializer,
    DisciplinaSerializer,
    CarreraSerializer,
    ModalidadSerializer,
    PerfilSerializer,
    ReservaSerializer
)

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer

class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

class ModalidadViewSet(viewsets.ModelViewSet):
    queryset = Modalidad.objects.all()
    serializer_class = ModalidadSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

class ReservaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reserva.objects.select_related('area', 'disciplina', 'carrera', 'modalidad', 'perfil').all()
    serializer_class = ReservaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        fecha_inicio = self.request.query_params.get('fecha_inicio')
        fecha_fin = self.request.query_params.get('fecha_fin')
        if fecha_inicio:
            queryset = queryset.filter(fecha_reserva__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_reserva__lte=fecha_fin)
        
        area_id = self.request.query_params.get('area_id')
        if area_id:
            queryset = queryset.filter(area_id=area_id)
        
        return queryset.order_by('fecha_reserva', 'hora_inicio')
            
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_excel(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            df = pd.read_excel(file, engine='openpyxl', header=2)
        except Exception:
            return Response(
                {'error': 'No se pudo leer el archivo Excel'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        df['FECHA DE RESERVA'] = pd.to_datetime(df['FECHA DE RESERVA']).dt.date

        min_date = df['FECHA DE RESERVA'].min()
        max_date = df['FECHA DE RESERVA'].max()

        today = timezone.now().date()

        errors = []

        with transaction.atomic():

            deleted_count = Reserva.objects.filter(fecha_reserva__lt=today).delete()[0]

            Reserva.objects.filter(fecha_reserva__gte=min_date, fecha_reserva__lte=max_date).delete()

            nuevas_reservas = []

            for index, row in df.iterrows():
                try:
                    perfil, _ = Perfil.objects.get_or_create(nombre=row['PERFIL'])
                    area, _ = Area.objects.get_or_create(nombre=row['AREA'])
                    disciplina, _ = Disciplina.objects.get_or_create(nombre=row['DISCIPLINA'])
                    carrera, _ = Carrera.objects.get_or_create(nombre=row['CARRERA'])
                    modalidad, _ = Modalidad.objects.get_or_create(nombre=row['MODALIDAD'])
                    nuevas_reservas.append(
                        Reserva(
                            area=area,
                            disciplina=disciplina,
                            carrera=carrera,
                            modalidad=modalidad,
                            perfil=perfil,
                            responsable=row['INSTRUCTORES'],
                            cedula=str(row['CÉDULA']).split('.')[0],
                            fecha_reserva=row['FECHA DE RESERVA'],
                            hora_inicio=row["HORA DE RESERVA"].split(" a ")[0].strip(),
                            hora_fin=row["HORA DE RESERVA"].split(" a ")[1].strip(),
                            actividad=row['ACTIVIDAD']
                        )
                    )
                except Exception as e:
                    errors.append({
                        'row': index+4,
                        'error': str(e)
                    })
            Reserva.objects.bulk_create(nuevas_reservas)
        return Response({
            'deleted_old': deleted_count,
            'created': len(nuevas_reservas),
            'errors': errors
        }, status=status.HTTP_201_CREATED)
    
