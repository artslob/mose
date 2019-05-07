from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wizards/', views.wizards, name='wizards'),
    path('wizards/<int:wizard_id>/', views.wizard_detail, name='wizard_detail'),
]
