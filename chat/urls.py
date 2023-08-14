from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('admin/', views.admin, name='admin'),
    path('delete/<int:message_id>', views.delete, name='delete'),
    path('logs/', views.logs, name='logs')
]