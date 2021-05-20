from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio import views

app_name = 'portfolio'

router = DefaultRouter()
router.register('', views.PortfolioViewSet)
router.register('sections/', views.SectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
