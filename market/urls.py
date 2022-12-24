from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.stocks_list),
    path('analyzed/', views.Stock_Analyze),
    path('get_data/',views.get_data),
    path('analyze_query/',views.analyze_volume_query)
    
    
    ] 