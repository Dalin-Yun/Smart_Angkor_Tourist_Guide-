from django.urls import path
from . import views

app_name = "guide"

urlpatterns = [
    path("", views.home, name="home"),
    path("temples/", views.temple_list, name="temple_list"),
    path("temples/<str:temple_id>/", views.temple_detail, name="temple_detail"),
    path("navigation/", views.navigation, name="navigation"),
    path("api/navigation/", views.navigation_api, name="navigation_api"),
    path("recommend/", views.recommend, name="recommend"),
]
