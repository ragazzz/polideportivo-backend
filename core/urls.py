from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    AreaViewSet,
    DisciplinaViewSet,
    CarreraViewSet,
    ModalidadViewSet,
    PerfilViewSet,
    ReservaViewSet
)

router = DefaultRouter()
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'disciplinas', DisciplinaViewSet, basename='disciplina')
router.register(r'carreras', CarreraViewSet, basename='carrera')
router.register(r'modalidades', ModalidadViewSet, basename='modalidad')
router.register(r'perfiles', PerfilViewSet, basename='perfil')
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = [
    path('api/', include(router.urls)),
]