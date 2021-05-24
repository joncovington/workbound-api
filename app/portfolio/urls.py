from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio import views

app_name = 'portfolio'

router = DefaultRouter()
router.register('portfolio/', views.PortfolioViewSet)
router.register('section/', views.SectionViewSet)
router.register('section/category/', views.SectionCategoryViewSet)
router.register('task/', views.TaskViewSet)
router.register('workitem/', views.WorkItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
