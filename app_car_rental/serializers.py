from rest_framework import serializers

from app_car_rental.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'name', 'dob', 'gender', 'contact_no_1', 'contact_no_2', 'email']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRate
        fields = '__all__'


class CategoryRateReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = CategoryRate
        fields = ['id', 'base_day_rental', 'kilometer_price', 'category']
        depth = 1


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['brand', 'model', 'category']


class CarReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Car
        fields = ['brand', 'model', 'category']
        depth = 1


class RentalRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalRegistration
        fields = '__all__'


class RentalRegistrationReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    class Meta:
        model = RentalRegistration
        fields = ['booking_number', 'customer', 'car']
        depth = 2


class CarBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBooking
        fields = '__all__'


class CarBookingReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBooking
        fields = '__all__'
        depth = 1


class CarReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarReturn
        fields = '__all__'


class CarReturnReadSerializer(serializers.ModelSerializer):
    rental_registration = RentalRegistrationReadSerializer()

    class Meta:
        model = CarReturn
        fields = ['car_return_id', 'return_datetime', 'current_milage_kms', 'rental_registration']
        depth = 2
