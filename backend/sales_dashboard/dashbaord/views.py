# sales/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Sales
from .serializers import SalesSerializer
import csv
from io import StringIO
from django.db.models import Sum, F
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer



class SalesViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Sales.objects.all()
        print(queryset)
        serializer = SalesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        print("------------------request",request.data)
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            print("--------------------------")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            sale = Sales.objects.get(pk=pk)
            serializer = SalesSerializer(sale)
            return Response(serializer.data)
        except Sales.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        print("Update Request Data:", request.data)
        try:
            sale = Sales.objects.get(pk=pk)
            print("=============request.data",request.data)
            serializer = SalesSerializer(sale, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Sales.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            sale = Sales.objects.get(pk=pk)
            sale.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Sales.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        print("CSV Upload Request Data:", request.data)
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return Response({"detail": "Invalid file format"}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        print("reader--",reader)
        # Strip BOM character from the first column header
        bom_removed_header = reader.fieldnames[0].lstrip('\ufeff')
        print("Fieldnames:", reader.fieldnames)
        for row in reader:
            print(row)
            
            Sales.objects.create(
                invoice_item_number=row['\ufeffInvoice/Item Number'] or row['Invoice/Item Number'],
                Date=row['Date'],
                store_number=row['Store Number'],
                store_name=row['store_name'],
                address=row['Address'],
                city=row['City'],
                zip_code=row['Zip Code'],
                store_location=row['Store Location'],
                county_number=row['County Number'],
                county=row['County'],
                category=row['Category'],
                category_name=row['category_name'],
                vendor_number=row['Vendor Number'],
                vendor_name=row['vendor_name'],
                item_number=row['Item Number'],
                item_desc=row['item_desc'],
                pack=row['Pack'],
                bottle_volume_ml=row['Bottle Volume (ml)'],
                state_bottle_cost=row['State Bottle Cost'],
                state_bottle_retail=row['State Bottle Retail'],
                bottles_sold=row['Bottles Sold'],
                sale_dollars=row['Sale (Dollars)'],
                volume_sold_liters=row['Volume Sold (Liters)'],
                volume_sold_gallons=row['Volume Sold (Gallons)']
            )

        return Response({"detail": "CSV data imported successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        print("------------request",request.data)
        print("-----------------------Query Parameters:", request.query_params)

        filters = {
            "store_name": request.query_params.get("store_name"),
        "city": request.query_params.get("city"),
        "zip_code": request.query_params.get("zip_code"),
        "store_location": request.query_params.get("store_location"),
        "county_number": request.query_params.get("county_number"),
        "category": request.query_params.get("category"),
        "category_name": request.query_params.get("category_name"),
        "vendor_number": request.query_params.get("vendor_number"),
        "vendor_name": request.query_params.get("vendor_name"),
        "item_number": request.query_params.get("item_number"),
        }
        sales = Sales.objects.all()

        for key, value in filters.items():
            if value:
                print("value--------",value)
                sales = sales.filter(**{key: value})

        aggregation_level = request.query_params.get("aggregat")
        print("aggregation_level------------",aggregation_level)

        aggregated_data = {}
        raw_data = []
        if aggregation_level:
            if aggregation_level == "city":
                aggregated_data = sales.values("city").annotate(
                    total_sales=Sum('sale_dollars'),
                    total_profit=Sum(F('sale_dollars') - F('state_bottle_cost')),
                    total_stock=Sum('bottles_sold')
                )
            elif aggregation_level == "county":
                aggregated_data = sales.values("county").annotate(
                    total_sales=Sum('sale_dollars'),
                    total_profit=Sum(F('sale_dollars') - F('state_bottle_cost')),
                    total_stock=Sum('bottles_sold')
                )
            elif aggregation_level == "zip_code":
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@222")
                aggregated_data = sales.values("zip_code").annotate(
                    total_sales=Sum('sale_dollars'),
                    total_profit=Sum(F('sale_dollars') - F('state_bottle_cost')),
                    total_stock=Sum('bottles_sold')
                )


        

        # Fetch overall total sales, total profit, and total stock
        overall_total_sales = sales.aggregate(total_sales=Sum('sale_dollars'))['total_sales'] or 0
        overall_total_profit = sales.aggregate(total_profit=Sum(F('sale_dollars') - F('state_bottle_cost')))['total_profit'] or 0
        overall_total_stock = sales.aggregate(total_stock=Sum('bottles_sold'))['total_stock'] or 0
        # Serialize the aggregated data
        serialized_aggregated_data = None
        if aggregated_data:
            serialized_aggregated_data = aggregated_data

        return Response({
           "overall_total_sales": overall_total_sales,
            "overall_total_profit": overall_total_profit,
            "overall_total_stock": overall_total_stock,
            "aggregated_data": serialized_aggregated_data
        })

# Login view
class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)