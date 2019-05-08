from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'wizuber'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='wizuber/login.html'), name='login'),
    path('customer/signup/', views.CustomerSignUp.as_view(), name='customer_signup'),
    path('wizards/', views.WizardsView.as_view(), name='wizards'),
    path('wizards/<int:pk>/', views.WizardDetail.as_view(), name='wizard_detail'),
]
