from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.stocks_list),
    path('get_latest_data', views.get_latest_data),
    path('analyzed_data', views.analyze_volume_data),
    path('get_data/<str:ticker>',views.get_data),
]