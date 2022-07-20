from django.urls import path
from .views import ProductListCreateView

app_name = 'items'

urlpatterns = [
    path('',ProductListCreateView.as_view()),

]