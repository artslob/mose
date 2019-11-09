from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic.base import TemplateView

import wizuber.views as views

app_name = 'wizuber'

urlpatterns = [
    path('', TemplateView.as_view(template_name='wizuber/index.html'), name='index'),

    path('account/', login_required(TemplateView.as_view(template_name='wizuber/account/detail.html')), name='account'),
    path('account/login/', auth_views.LoginView.as_view(template_name='wizuber/account/login.html'), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/signup/', views.account.CustomerSignUp.as_view(), name='signup'),

    path('wizard/list/', views.wizard.ListWizard.as_view(), name='wizards'),
    path('wizard/<int:pk>/', views.wizard.DetailWizard.as_view(), name='wizard_detail'),

    path('wish/list/', views.wish.ListWish.as_view(), name='wishes'),
    path('wish/create/', views.wish.CreateWish.as_view(), name='create_wish'),
    path('wish/<int:pk>/', views.wish.DetailWish.as_view(), name='wish_detail'),
    path('wish/<int:pk>/fulfill', views.wish.FulfillWish.as_view(), name='fulfill_wish'),
]
