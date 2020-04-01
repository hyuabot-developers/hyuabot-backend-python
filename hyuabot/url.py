from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chatbot'),
    path('shuttlephoto', views.shuttlephoto),
    path('shuttle', views.shuttle),
    path('food', views.food),
    path('lib', views.library),
    path('restphoto', views.restphoto),
    path('phone', views.phone_search),
    path('club', views.club),
    path('circle', views.circle),
    path('clubinfo', views.info)
]