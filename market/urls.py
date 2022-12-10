from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.stocks_list),
    path('get_latest_data', views.get_latest_data),
    path('analyzed_data', views.analyze_volume_data),
    path('get_data/',views.get_data),
    path("duplicate_row/",views.delete_duplicate_rows),
    path("check_dup",views.get_duplicates)

]