from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'wizuber'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', login_required(TemplateView.as_view(template_name='wizuber/account.html')), name='account'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='wizuber/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.CustomerSignUp.as_view(), name='signup'),
    path('wizards/', views.WizardsView.as_view(), name='wizards'),
    path('wizards/<int:pk>/', views.WizardDetail.as_view(), name='wizard_detail'),
]
