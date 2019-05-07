from django.urls import path

from . import views

app_name = 'wizuber'
urlpatterns = [
    path('', views.index, name='index'),
    path('wizards/', views.WizardsView.as_view(), name='wizards'),
    path('wizards/<int:wizard_id>/', views.wizard_detail, name='wizard_detail'),
]
