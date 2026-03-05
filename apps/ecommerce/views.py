from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    )
from rest_framework.response import Response
from rest_framework import status
from apps.items.models import Product
from apps.categories.models import Category
from .serializers import (
    ProductSerializer,
    ShortProductSerializer,
    )
from .permissions import IsSellerOrReadOnly
from django.http import Http404
from .paginators import LargeResultsSetPagination
from django.db.models import Q

class ProductListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        q = request.query_params.get('q', '').strip()
        cat_name = request.query_params.get("cat")
        
        products = Product.objects.select_related("seller").filter(visibility="pu")

        if cat_name:
            try:
                category = Category.objects.get(name=cat_name)
                category_ids = category.children.values_list('id', flat=True)
                products = products.filter(
                    Q(categories=category) | Q(categories__id__in=category_ids)
                )
            except Category.DoesNotExist:
                return Response({'data': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        if q:
            products = products.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(categories__name__icontains=q)
            ).distinct()

        if products.exists(): # .exists() is faster than len()
            paginator = LargeResultsSetPagination()
            paginated_q = paginator.paginate_queryset(products, request)
            serializer = ShortProductSerializer(paginated_q, many=True, read_only=True, context={"request":request})
            return paginator.get_paginated_response(data={'data': serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'data': 'There are no products'}, status=status.HTTP_204_NO_CONTENT)


class ProductDetailAPIView(APIView):
    permission_classes = [IsSellerOrReadOnly, ]
    def get_object(self, slug:str):
        try:
            obj = Product.objects.get(slug=slug)
            self.check_object_permissions(self.request, obj)
            return obj
        except:
            raise Http404("You are not allowed modify this product")
        
    def get(self, request, format=None, *args, **kwargs):
        product = self.get_object(kwargs["slug"])
        if not product.visibility == 'pr' or request.user.customer == product.seller or request.user.is_superuser:
            serializer = ProductSerializer(instance=product, context={"request":request})
            return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"error":"You are not authorized to see this article"}, status=status.HTTP_401_UNAUTHORIZED)


    
    def patch(self, request, format=None, *args, **kwargs):
        product = self.get_object(kwargs["slug"])
        serializer = ProductSerializer(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={"product":serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def delete(self, request, format=None, *args, **kwargs):
        product = self.get_object(kwargs["slug"])
        product.delete()
        return Response(data={"data":"deleted"}, status=status.HTTP_200_OK)
