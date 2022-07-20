from itertools import product
from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics , permissions , status
from rest_framework.response import Response



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Product.objects.all()
        sort_by = self.request.query_params.get('sort_by', None)
        if sort_by is not None:
            if sort_by == 'price':
                queryset = queryset.order_by('price')
            elif sort_by == 'name':
                queryset = queryset.order_by('name')
        filter_by = self.request.query_params.get('price', None)
        
        if filter_by is not None:
            queryset = queryset.filter(price=filter_by)
        return queryset



