from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="blog"),
    path('blogpost/<int:id>', views.blogpost, name="blogPost"),
]