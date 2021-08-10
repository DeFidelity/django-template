from django.urls import path
from landing import views

urlpatterns = [
    path('',views.Index.as_view(), name='index'),
]
