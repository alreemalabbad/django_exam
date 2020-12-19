from django.urls import path     
from . import views

urlpatterns = [
    # render
    path('', views.index),
    path('wishes', views.dashboard),
    path('wishes/new', views.view_create),
    path('edit/<int:wish_id>', views.view_edit),
    path('wishes/status', views.view_status),
    # redirect
    path('register', views.register),
    path('logout',views.logout),
    path('login', views.login),
    path('create', views.create),
    path('remove/<int:wish_id>', views.remove),
    path('update/<int:wish_id>', views.update),
    path('granted/<int:wish_id>', views.granted),
    path('like/<int:wish_id>', views.like),
    path('unlike/<int:wish_id>', views.unlike),
]