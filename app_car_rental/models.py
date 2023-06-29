import uuid

from django.db import models
from django.contrib.auth.models import User


class LogModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Customer(LogModel):
    CH_GENDER = (
        ('Male', 'Male'), ('Female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField('name', max_length=255)
    dob = models.DateField('dob')
    gender = models.CharField('gender', max_length=10, choices=CH_GENDER)
    contact_no_1 = models.CharField('contact no.1', max_length=15)
    contact_no_2 = models.CharField('contact no.1', max_length=15, blank=True, default='')
    email = models.EmailField('email', max_length=255, unique=True)


class Category(LogModel):
    name = models.CharField('name', max_length=60, unique=True, blank=False, null=False)


class CategoryRate(LogModel):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='category_rate')
    base_day_rental = models.FloatField('base day rental')
    kilometer_price = models.FloatField('kilometer price')


class Car(LogModel):
    brand = models.CharField('brand', max_length=60)
    model = models.CharField('model', max_length=60)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars')

    class Meta:
        unique_together = ['brand', 'model']


class RentalRegistration(LogModel):
    booking_number = models.UUIDField('booking number', primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rental_registrations')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rental_registrations')


class CarBooking(LogModel):
    rental_registration = models.OneToOneField(RentalRegistration, on_delete=models.CASCADE, related_name='car_booking')
    booking_datetime = models.DateTimeField('rental date & time')
    car_milage_kms = models.FloatField('car milage in Km')


class CarReturn(LogModel):
    car_return_id = models.UUIDField('car return id', primary_key=True, default=uuid.uuid4, editable=False)
    rental_registration = models.OneToOneField(RentalRegistration, on_delete=models.CASCADE, related_name='car_return')
    return_datetime = models.DateTimeField('return date & time')
    current_milage_kms = models.FloatField('car milage in Km')

    def calculate_bill(self):
        bill_d = {}

        try:
            category = self.rental_registration.car.category
            category_rate = category.category_rate

            bill_d = {
                'billing_amount': 0.0,
                'prev_car_milage': self.rental_registration.car_booking.car_milage_kms,
                'curr_car_milage': self.current_milage_kms,
                'number_of_kms': self.current_milage_kms - self.rental_registration.car_booking.car_milage_kms,
                'car_category': category.name,
                'base_day_rental': category_rate.base_day_rental,
                'kilometer_price': category_rate.kilometer_price
            }

            bill_d['number_of_kms'] = bill_d['curr_car_milage'] - bill_d['prev_car_milage']
            booking_datetime = self.rental_registration.car_booking.booking_datetime
            number_of_days = (self.return_datetime - booking_datetime).days

            if str(category.name).lower() == 'compact':
                bill_d['billing_amount'] = bill_d['base_day_rental'] * number_of_days
            elif str(category.name).lower() == 'premium':
                bill_d['billing_amount'] = bill_d['base_day_rental'] * number_of_days * 1.2 + bill_d['kilometer_price'] + bill_d['number_of_kms']
            elif str(category.name).lower() == 'minivan':
                bill_d['billing_amount'] = bill_d['base_day_rental'] * number_of_days * 1.7 + (bill_d['kilometer_price'] + bill_d['number_of_kms'] * 1.5)
            else:
                raise Exception('Invalid Car Category!')
        except Exception as e:
            print(e)

        return bill_d



