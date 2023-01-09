from django.urls import path
from . import views
from . import models




urlpatterns = [
    path('stocks/', views.stocks_list),
    path('analyzed/', views.Stock_Analyze),
    path('get_data/',views.get_data),
    path('analyze_query/',views.analyze_volume_query),
    path('ticker_list', views.ticker_list),
    path("user_ticker", views.add_user_stock)
    
    ] 