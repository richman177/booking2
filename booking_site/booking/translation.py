from .models import Hotel, Room, Country, City
from modeltranslation.translator import TranslationOptions, register


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'hotel_description','address')


@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('room_description',)
