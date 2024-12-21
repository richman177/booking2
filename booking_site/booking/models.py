from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('simpleUser', 'simpleUser'),
        ('ownerUser', 'ownerUser')
    )
    user_role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='simpleUser')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),MaxValueValidator(100)],
                                           null=True, blank=True)


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.country_name}'


class City(models.Model):
    city_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.city_name}'


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=32)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel_description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='hotels')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    address = models.CharField(max_length=32)
    hotel_stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                                MaxValueValidator(5)])
    hotel_video = models.FileField(upload_to='hotel_image/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.hotel_name}, {self.country}, {self.city}'

    def get_avg_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return round(sum([i.room_stars for i in ratings]) / ratings.count(), 1)
        return 0


    def get_count_people(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_images')
    hotel_image = models.ImageField(upload_to='hotel_image/')


class Room(models.Model):
    room_number = models.PositiveSmallIntegerField()
    hotel_room = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    TYPE_CHOICES = (
        ('люкс', 'люкс'),
        ('семейный', 'семейный'),
        ('одноместный', 'одноместный'),
        ('двухместный', 'двухместный'),
    )
    room_type = models.CharField(choices=TYPE_CHOICES, max_length=32)

    STATUS_CHOICES = (
        ('свободен', 'свободен'),
        ('занят', 'занят'),
        ('забронирован', 'забронирован'),
    )
    room_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='свободен')
    room_price = models.PositiveIntegerField()
    all_inclusive = models.BooleanField(default=True)
    room_description = models.TextField()

    def __str__(self):
        return f'{self.hotel_room}, {self.room_number},{self.room_type}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    room_image = models.ImageField(upload_to='room_images/')


class Review(models.Model):
    user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(null=True, blank=True)
    room_stars = models.IntegerField (max_length=20, choices=[(i, str(i))for i in range(1,6)], null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user_name}, {self.hotel}, {self.room_stars}'

    class Meta:
        unique_together =('user_name', 'hotel',)


class Booking(models.Model):
    hotel_book = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_book = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_book = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    totel_price = models.PositiveIntegerField(default=0)
    STATUS_BOOK_CHOICES = (
        ('отменено', 'отменено'),
        ('подеверждено', 'подеверждено')

    )
    status_book = models.CharField(max_length=32, choices=STATUS_BOOK_CHOICES)

    def __str__(self):
        return f'{self.user_book}, {self.hotel_book}, {self.room_book}, {self.status_book}'