from django.contrib import admin
from django.urls import path, include

import water.views
import hoteladmin.views
from water.views import *

urlpatterns = [
    path('', hoteladmin.views.LoadDashboard, name='LoadAdmin'),
    path('deletebottledetails', hoteladmin.views.DeleteBottleDetails, name='DeleteBottleDetails'),
    path('createbrand', hoteladmin.views.CreateBrand, name='CreateBrand'),
    path('deletebrand', hoteladmin.views.DeleteBrand, name='DeleteBrand'),
    path('createsize', hoteladmin.views.CreateSize, name='CreateSize'),
    path('deletesize', hoteladmin.views.DeleteSize, name="DeleteSize"),
    path('dashboard', hoteladmin.views.LoadDashboard, name='LoadDashboard'),

]
