from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ReceiptViewSet, ItemViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet,basename = 'category')
router.register('receipts', ReceiptViewSet,basename = 'receipt')
router.register('items', ItemViewSet,basename = 'item')

urlpatterns = [
    path('', include(router.urls)),
]