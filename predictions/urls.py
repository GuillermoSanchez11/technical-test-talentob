from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('docs/', views.swagger_docs, name='swagger_docs'),
]
