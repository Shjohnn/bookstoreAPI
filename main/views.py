from math import acosh

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.shortcuts import *

from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import *
from rest_framework.fields import *


class BookPagination(PageNumberPagination):
    page_size = 12  # Har bir sahifada 12 ta obyekt bo‘ladi
    page_size_query_param = 'page_size'  # URL orqali sahifa hajmini o‘zgartirishga ruxsat
    max_page_size = 13152


class RegisterAPIVIew(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class BooksListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cover', 'sold', 'account', ]
    search_fields = ['title']
    ordering_fields = ['title', 'price', 'created_at']
    pagination_class = BookPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='sold',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='Filter books by sales'

            ),
            openapi.Parameter(
                name='account',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by account'
            ),
            openapi.Parameter(
                name='cover',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by cover'
            ),

        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookSerilazier
        return BookPostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookSerilazier
        return BookPostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):

        if serializer.instance.account != self.request.user:
            raise PermissionDenied(detail='You are not owner of this book')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.account != self.request.user:
            raise PermissionDenied(detail='You are not owner of this book')
        instance.delete()


class MyBooksList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerilazier

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sold', 'cover', ]
    search_fields = ['title', ]
    ordering_fields = ['title', 'price', 'created_ad']
    pagination_class = BookPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='sold',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='Filter books by sales'

            ),
            openapi.Parameter(
                name='account',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by account'
            ),
            openapi.Parameter(
                name='cover',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by cover'
            ),

        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return Book.objects.filter(account=self.request.user)


class BookMarkSoldAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk,account=self.request.user)
        serializer =BookMarkSoldSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save(sold=True)
            response={
                'succes':True,
                'message':'book marked sold',
                'data':BookSerilazier(book).data

            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MyWishlistListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookSerilazier
#
#     def get_queryset(self):
#         account=self.request.user
#         return self.request.user.wishlist.books.order_by('title')



