from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list_create, name='user_list_create')
]
