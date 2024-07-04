from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from customers.api.serializers import CustomerSerializer, CustomerSmallSerializer, RecordSerializer, NotesSerializer
from customers.models import Customer, Record, Notes, Version
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django.utils import timezone
from django.db.models import Sum
from rest_framework.decorators import action
from django.utils.dateparse import parse_date

class GetVersion(APIView):
    def get(self, request):
        version = Version.objects.all().first().version
        return Response({'version': version}, status=status.HTTP_200_OK)

class CustomerPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(is_active=True).order_by('amount').order_by('id')
    serializer_class = CustomerSerializer
    # pagination_class = CustomerPagination

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
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    search_fields = ['id', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('amount', 'id')
        return queryset
    
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        day = self.request.query_params.get('day', None)
        if day:
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
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if is_refund :
            queryset = queryset.filter(is_refund=is_refund)
        
        if date_from and date_to :
            date_from_parsed = parse_date(date_from)
            date_to_parsed = parse_date(date_to)
            if date_from_parsed and date_to_parsed:
                queryset = queryset.filter(created_at__range=[date_from_parsed, date_to_parsed])
        
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
        queryset = self.get_queryset().filter(created_at__year=date.year, created_at__month=date.month, created_at__day=date.day, collector=request.user).order_by('-created_at')
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


class NotesViewSet(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    queryset = Notes.objects.all().order_by('-id')
    filter_backends = [SearchFilter, DjangoFilterBackend] 
    search_fields = ['customer__name', 'note']


    # TODO add filter by note_type
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        is_solved = self.request.query_params.get('is_solved', None)
        if is_solved :
            queryset = queryset.filter(is_solved=is_solved)
        return queryset.order_by('-id')

# # Seed data
import random

arabic_names = [
    "طارق",
    "سلمى",
    "محمود",
    "جوان",
    "مرام",
    "عبداللطيف",
    "هاجر",
    "محمد",
    "رحمة",
    "سعيد",
    "حنان",
    "إيمان",
    "سليمان",
    "دانا",
    "عبدالمجيد",
    "فرح",
    "رامي",
    "سمية",
    "عبدالوهاب",
    "زينة",
    "عبدالحميد",
    "ندى",
    "خلود",
    "محمد",
    "ريان",
    "رباب",
    "أحلام",
    "عبدالقادر",
    "شهد",
    "سامر",
    "داليا",
    "فادي",
    "جميلة",
    "عبدالله",
    "ميس",
    "حسام",
    "سهى",
    "علياء",
    "ياسر",
    "لبنى",
    "عماد",
    "رغد",
    "مجد",
    "سارة",
    "يزن",
    "نورهان",
    "محمد",
    "شيماء",
    "ناصر",
    "مريم",
    "عبدالرؤوف",
    "مريانا",
    "عبدالحليم",
    "مي",
    "محمد",
    "سناء",
    "جمال",
    "رنيم",
    "عبدالرزاق",
    "داليا",
    "سمير",
    "نوران",
    "حازم",
    "آية",
    "عبدالكريم",
    "ملك",
    "أنس",
    "ريما",
    "عبدالغني",
    "ليلى"
]
addresses = [
    20,
    21,
    22,
]
from django.shortcuts import HttpResponse

def create_names(request):
    for n in arabic_names:
        address = random.choice(addresses)
        collect_day = random.randint(1, 28)
        try:
            Customer.objects.create(
                name=n,
                address_id=address,
                collect_day=collect_day,
            )
        except:
            pass
    return HttpResponse("done")    
