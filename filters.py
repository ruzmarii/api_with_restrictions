import django_filters
from django_filters import DateFromToRangeFilter
from .models import Advertisement, AdvertisementStatusChoices

class AdvertisementFilter(django_filters.FilterSet):
    """Фильтры для объявлений"""
    created_at = DateFromToRangeFilter()
    status = django_filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    
    class Meta:
        model = Advertisement
        fields = ['status', 'created_at', 'creator']