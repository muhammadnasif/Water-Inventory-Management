from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoadHome, name='load_home'),
    path('home', views.LoadHome, name='load_home'),
    path('status', views.LoadStatus, name='load_status'),
    path('sellBottleMethod', views.sellBottleMethod, name='sellBottleMethod'),
    # path('newBottleForm', views.newBottleMethod, name='newBottleMethod'),
    path('addNewStock', views.addNewStockMethod, name='addNewStockMethod'),
    path('createNewBottle', views.createNewBottleMethod, name='createNewBottleMethod'),
    path('filtersearch', views.FilterSearch, name='FilterSearch'),
    path('historydetailsundo', views.HistoryDetailsUndo, name='HistoryDetailsUndo'),
    path('sellbottlecomplimentary', views.sellBottleComplimentary, name='sellBottleComplimentary'),
]
