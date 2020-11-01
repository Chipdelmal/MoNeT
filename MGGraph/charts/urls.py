from django.urls import path
from . import views


app_name = 'charts'

urlpatterns = [
    path('', views.index, name='index'),
    path('graph/<csv>/<color_csv>/<ftype>', views.graph, name='graph'),
    path('graph/<csv>/<csv_2>', views.graph_2, name='graph_2')
]
