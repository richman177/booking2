from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserProfileSeriaLizer(serializers.ModelSerializer):
      class Meta:
          model = UserProfile
          fields =('username', 'email', 'password', 'first_name', 'last_name',
                'age', 'phone_number', 'user_role')
          extra_kwargs = {'password': {'write_only': True}}

      def create(self, validated_data):
          user = UserProfile.objects.create_user(**validated_data)
          return user

      def to_representation(self, instance):
          refresh = RefreshToken.for_user(instance)
          return {
              'user': {
                  'username': instance.username,
                  'email': instance.email,
              },
              'access': str(refresh.access_token),
              'refresh': str(refresh),

          }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),

        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['hotel_image']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class HotelListSerializer(serializers.ModelSerializer):
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    city = CityListSerializer()

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name','city', 'address', 'hotel_stars', 'hotel_images', 'avg_rating', 'get_count_people']

    def get_avg_rating(self, obg):
        return obg.get_avg_rating()



    def get_count_people(self, obg):
        return obg.get_count_people()


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name',]


class CountryDetailSerializer(serializers.ModelSerializer):
    hotels = HotelListSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['country_name', 'hotels']


class CityDetailSerializer(serializers.ModelSerializer):
    hotels = HotelListSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ['city_name', 'hotels']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['room_image']


class RoomListSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'room_status', 'room_price', 'room_images']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = UserProfileSimpleSerializer()

    class Meta:
        model = Review
        fields = ['user_name', 'text', 'parent', 'room_stars']


class HotelDetailSerializer(serializers.ModelSerializer):
    country = CountryListSerializer()
    city = CityListSerializer()
    owner = UserProfileSimpleSerializer()
    created_date = serializers.DateField(format('%d-%m-%Y'))
    hotel_images = HotelImageSerializer(many=True, read_only=True)
    rooms = RoomListSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['hotel_name', 'hotel_description', 'country', 'city', 'address', 'hotel_images','hotel_video',
                  'owner', 'created_date', 'hotel_stars', 'rooms', 'reviews']


class RoomDetailSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'room_status', 'room_price', 'all_inclusive', 'room_description', 'room_images']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
