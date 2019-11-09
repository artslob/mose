from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'wizuber'

urlpatterns = [
    path('', TemplateView.as_view(template_name='wizuber/index.html'), name='index'),

    path('account/', login_required(TemplateView.as_view(template_name='wizuber/account/detail.html')), name='account'),
    path('account/login/', auth_views.LoginView.as_view(template_name='wizuber/account/login.html'), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/signup/', views.CustomerSignUp.as_view(), name='signup'),

    path('wizards/', views.WizardsView.as_view(), name='wizards'),
    path('wizards/<int:pk>/', views.WizardDetail.as_view(), name='wizard_detail'),

    path('wishes/', views.WishesList.as_view(), name='wishes'),
    path('wishes/new/', views.CreateWish.as_view(), name='create_wish'),
    path('wishes/<int:pk>/', views.WishDetail.as_view(), name='wish_detail'),
    path('wishes/<int:pk>/fulfill', views.FulfillWish.as_view(), name='fulfill_wish'),
]
