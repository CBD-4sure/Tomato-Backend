
from django.urls import path
from . import views

urlpatterns= [
    path('',views.ResDataApi.as_view(),name='resDataApi'),
    path('m/<int:resId>',views.MenuDataApi.as_view(),name='menuDataApi')

]