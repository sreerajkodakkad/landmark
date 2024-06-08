# sales/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# router.register(r'sales', SalesViewSet, basename='sales')

urlpatterns = [
    path('sales/', SalesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sales/<int:pk>/', SalesViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', SalesViewSet.as_view({'get': 'dashboard'}), name='dashboard'),  # Add this line
    path('upload_csv/', SalesViewSet.as_view({'post': 'upload_csv'}), name='upload-csv'),


]
