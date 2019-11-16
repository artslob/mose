from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import TemplateView

import wizuber.views as views

app_name = 'wizuber'

urlpatterns = [
    path('', TemplateView.as_view(template_name='wizuber/index.html'), name='index'),

    path('account/', views.account.DetailAccount.as_view(), name='account'),
    path('account/login/', views.account.LoginAccount.as_view(), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/signup/', views.account.CustomerSignUp.as_view(), name='signup'),

    path('wizard/list/', views.wizard.ListWizard.as_view(), name='list-wizard'),
    path('wizard/<int:pk>/', views.wizard.DetailWizard.as_view(), name='detail-wizard'),

    path('wish/list/', views.wish.ListWish.as_view(), name='list-wish'),
    path('wish/list/active', views.wish.ListWishActive.as_view(), name='list-wish-active'),
    path('wish/create/', views.wish.CreateWish.as_view(), name='create-wish'),
    path('wish/<int:pk>/', views.wish.DetailWish.as_view(), name='detail-wish'),
    path('wish/<int:pk>/handle/<str:action>', views.wish.HandleWishAction.as_view(), name='handle-wish-action'),
    path('wish/<int:pk>/fulfill', views.wish.FulfillWish.as_view(), name='fulfill-wish'),
]
