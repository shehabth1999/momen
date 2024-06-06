from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status, generics
from customers.api.serializers import CustomerSerializer, CustomerSmallSerializer, RecordSerializer
from customers.models import Customer, Record
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.utils import timezone
from django.db.models import Sum
from rest_framework.decorators import action


class CustomerPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(is_active=True).order_by('id')
    serializer_class = CustomerSerializer
    pagination_class = CustomerPagination

    # stop deleting
    def delete(self, request, pk):
        return Response({'message': 'Cant delete'}, status=status.HTTP_403_FORBIDDEN)
    
    # stop editing
    def update(self, request, pk):
        return Response({'message': 'Cant edit'}, status=status.HTTP_403_FORBIDDEN)

    # stop editing
    def partial_update(self, request, pk):
        return Response({'message': 'Cant edit'}, status=status.HTTP_403_FORBIDDEN)
    
    


class CustomerSmallView(generics.ListAPIView):
    queryset = Customer.objects.filter(is_active=True).order_by('id')
    serializer_class = CustomerSmallSerializer
    filter_backends = [SearchFilter] 
    search_fields = ['id', 'name']

    def filter_queryset(self, queryset):
        day = self.request.query_params.get('day', None)
        if day :
            queryset = queryset.filter(collect_day=day)
        return queryset
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        day = request.query_params.get('day', None)
        if day:
            total_amount = self.filter_queryset(self.get_queryset()).aggregate(Sum('amount'))['amount__sum'] or 0
            response.data['total_amount'] = total_amount
        return response



class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    queryset = Record.objects.all().order_by('id')
    filter_backends = [SearchFilter]    
    search_fields = ['customer__name', 'collector__username']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        is_refund = self.request.query_params.get('is_refund', None)
        if is_refund :
            queryset = queryset.filter(is_refund=is_refund)
        return queryset
    

    # stop deleting
    def delete(self, request, pk):
        return Response({'message': 'Cant delete'}, status=status.HTTP_403_FORBIDDEN)
    
    # stop editing
    def update(self, request, pk):
        return Response({'message': 'Cant edit'}, status=status.HTTP_403_FORBIDDEN)

    # stop editing
    def partial_update(self, request, pk):
        return Response({'message': 'Cant edit'}, status=status.HTTP_403_FORBIDDEN) 
    
    @action(detail=False, methods=['get'], url_path='records-today')
    def records_today(self, request):
        date = timezone.now().date()
        queryset = self.get_queryset().filter(created_at__year=date.year, created_at__month=date.month, created_at__day=date.day)
        serializer = self.get_serializer(queryset, many=True)
        total_amount = queryset.aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({'count': queryset.count(), 'total_amount':total_amount, 'records': serializer.data, }, status=status.HTTP_200_OK)


class Arrears(generics.ListAPIView):
    day = timezone.now().day
    queryset = Customer.objects.filter(is_active=True, collect_day__lt=day, amount__gt=0).order_by('-collect_day')
    serializer_class = CustomerSmallSerializer
    filter_backends = [SearchFilter] 
    search_fields = ['id', 'name']


    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        day = self.request.query_params.get('day', None)
        if day :
            queryset = queryset.filter(collect_day=day)
        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Calculate the sum of the amount values for the filtered queryset
        total_amount = self.filter_queryset(self.get_queryset()).aggregate(Sum('amount'))['amount__sum'] or 0
        response.data['total_amount'] = total_amount
        return response

