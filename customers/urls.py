from rest_framework.routers import DefaultRouter
from django.urls import path, include
from customers.api.views import CustomerViewSet, CustomerSmallView, RecordViewSet, NotesViewSet, CustomerValueViewSet, new_customer_month


router = DefaultRouter()
router.register(r'list', CustomerViewSet)
router.register(r'record', RecordViewSet)
router.register(r'notes', NotesViewSet)
router.register(r'value', CustomerValueViewSet)

urlpatterns = [
    path('', CustomerSmallView.as_view(), name='customers-small'),
    path('', include(router.urls)),
    path('new_month/', new_customer_month, name='new_month'),
]