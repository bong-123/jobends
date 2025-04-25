from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import  Company,  Position
from .serializers import CompanySerializer, PositionSerializer




# Position Views
class PositionListCreateView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
# Company Views

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyByJobCategoryView(APIView):
    def get(self, request, jobcategory):
        companies = Company.objects.filter(position__jobcategory=jobcategory)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)
    
class CompanyDetailAPIView(APIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer



