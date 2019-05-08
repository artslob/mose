from django.urls import path

from . import views

app_name = 'wizuber'
urlpatterns = [
    path('', views.index, name='index'),
    path('customer/signup/', views.CustomerSignUp.as_view(), name='customer_signup'),
    path('wizards/', views.WizardsView.as_view(), name='wizards'),
    path('wizards/<int:pk>/', views.WizardDetail.as_view(), name='wizard_detail'),
]
