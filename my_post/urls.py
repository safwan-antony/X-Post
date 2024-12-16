from django.urls import path 
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('comment/<int:pk>/', comment, name='comment'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('delete-comment/<int:pk>/', delete_comment, name='delete_comment'),
    path('edit-comment/<int:pk>/', edit_comment, name='edit_comment'),

]