from django.urls import path
from . import views
urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('add/', views.subject_add, name='subject_add'),
    path('<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('<int:pk>/delete/', views.subject_delete, name='subject_delete'),
]
