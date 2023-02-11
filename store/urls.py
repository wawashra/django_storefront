from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

simple_router = SimpleRouter()

simple_router.register('products', views.ProductModelViewSet)
simple_router.register('collections', views.CollectionModelViewSet)
# URLConf
urlpatterns = simple_router.urls

# [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view(), name='collections'),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
# ]
