from rest_framework.routers import DefaultRouter
from django.urls import path, include
from customers.api.views import CustomerViewSet, CustomerSmallView, RecordViewSet


router = DefaultRouter()
router.register(r'list', CustomerViewSet)
router.register(r'record', RecordViewSet)

urlpatterns = [
    path('', CustomerSmallView.as_view(), name='customers-small'),
    path('', include(router.urls)),
]