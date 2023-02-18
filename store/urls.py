from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductModelViewSet, basename='products')
router.register('collections', views.CollectionModelViewSet)
router.register('carts', views.CartModelViewSet)
router.register('customers', views.CustomerViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewModelViewSet, basename='product-reviews')


cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemModelViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + products_router.urls + cart_router.urls

# [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view(), name='collections'),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail')
# ]
