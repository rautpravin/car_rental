from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app_car_rental.models import *
from app_car_rental.serializers import *


class CustomerRegViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarReadSerializer
        return CarSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer_class()(data=request.data, many=True)
        if ser.is_valid(raise_exception=True):
            recs = ser.save()
            ser = self.get_serializer_class()(recs, many=True)
            return Response(ser.data, status=status.HTTP_201_CREATED)


class CategoryRateViewSet(viewsets.ModelViewSet):
    queryset = CategoryRate.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryRateReadSerializer
        return CategoryRateSerializer


class RentalRegistrationViewSet(viewsets.ModelViewSet):
    queryset = RentalRegistration.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RentalRegistrationReadSerializer
        return RentalRegistrationSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer_class()(data=request.data)
        if ser.is_valid(raise_exception=True):
            o = ser.save()
            return Response(RentalRegistrationReadSerializer(o).data, status=status.HTTP_201_CREATED)


class CarBookingViewSet(viewsets.ModelViewSet):
    queryset = CarBooking.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarBookingReadSerializer
        return CarBookingSerializer


class CarReturnViewSet(viewsets.ModelViewSet):
    queryset = CarReturn.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarReturnReadSerializer
        return CarReturnSerializer


def calculate_bill_viewset(request, pk=None):

    try:
        car_return = CarReturn.objects.get(rental_registration_id=pk)
        d = car_return.calculate_bill()
        import json
        return JsonResponse(d)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








