from rest_framework import viewsets, status,  generics
from .models import *
from .serializers import *
from .filters import HotelFilter, RoomFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CheckCreateHotel
from .paginations import HotelNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSeriaLizer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer


class CountryDetailAPIView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializer



class HotelListAPIView (generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HotelFilter
    search_fields = ['hotel_name']
    ordering_fields = ['stars']
    pagination_class = HotelNumberPagination



class HotelDetailAPIView (generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelDetailSerializer


class HotelCreateAPIView(generics.CreateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [CheckCreateHotel]


class HotelEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [CheckCreateHotel]

    def get_queryset(self):
        return Hotel.objects.filter(owner=self.request.user)




class HotelImageViewSet(viewsets.ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer

class RoomCreateAPIView(generics.CreateAPIView):
    serializer_class = RoomSerializer



class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer


class RoomEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        return Room.objects.filter(owner=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer


class CityDetailAPIView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
