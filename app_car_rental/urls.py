from django.urls import path
from rest_framework import routers

from app_car_rental import viewsets

router = routers.SimpleRouter()

router.register(r'cust-register', viewsets.CustomerRegViewSet)

router.register(r'category', viewsets.CategoryViewSet)
router.register(r'category-rate', viewsets.CategoryRateViewSet)

router.register(r'car', viewsets.CarViewSet)

router.register(r'rental-reg', viewsets.RentalRegistrationViewSet)

router.register(r'car-booking', viewsets.CarBookingViewSet)
router.register(r'car-return', viewsets.CarReturnViewSet)


urlpatterns = [
    path('cal-bill/<str:pk>/', viewsets.calculate_bill_viewset)
]

urlpatterns += router.urls

