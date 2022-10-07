from django.urls import path
from . import views

urlpatterns = [
    path('', views.userhome),
    path('funds/', views.funds),
    path('payment/', views.payment),
    path('success/', views.success),
    path('cancel/', views.cancel)
]
