from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graph/<csv>', views.graph, name='graph'),
    path('graph/<csv>/<csv_2>', views.graph_2, name='graph_2')
]
