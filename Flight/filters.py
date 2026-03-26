import django_filters
from .models import Flight,Airport,Destination
from django.db.models.functions import ExtractHour
from django.http import QueryDict

class Airport_filter(django_filters.FilterSet):
    min_rate = django_filters.NumberFilter(field_name='rate',lookup_expr='gte')
    max_rate = django_filters.NumberFilter(field_name='rate',lookup_expr='lte')
    class Meta:
        model = Airport
        fields = ['destination']



class Destination_filter(django_filters.FilterSet):
    
    min_static_rate = django_filters.NumberFilter(field_name='static_rate',lookup_expr='gte')
    max_static_rate = django_filters.NumberFilter(field_name='static_rate',lookup_expr='lte')
    min_avg_rate = django_filters.NumberFilter(field_name='avg_rate',lookup_expr='gte')
    max_avg_rate = django_filters.NumberFilter(field_name='avg_rate',lookup_expr='lte')
    
    class Meta:
        model = Destination
        fields = ['country','is_top_destination']
    


class flights_filter(django_filters.FilterSet):
    
    type = django_filters.CharFilter(field_name='type',lookup_expr='iexact')
    has_economy = django_filters.BooleanFilter(method='filter_has_economy')
    has_premium_economy = django_filters.BooleanFilter(method='filter_has_premium_economy')
    has_business = django_filters.BooleanFilter(method='filter_has_business')
    has_first_class = django_filters.BooleanFilter(method='filter_has_first_class')
    scheduled_departure_minimum_date = django_filters.DateFilter(
        field_name='scheduled_departure',
        lookup_expr='date__gte'
    )
    scheduled_arrival_maximum_date = django_filters.DateFilter(
        field_name='scheduled_arrival',
        lookup_expr='date__lte'
    )
    scheduled_departure_time_range_min = django_filters.NumberFilter(
        method='filter_departure_time_min'
    )
    scheduled_departure_time_range_max = django_filters.NumberFilter(
        method='filter_departure_time_max'
    )
    scheduled_arrival_time_range_min = django_filters.NumberFilter(
        method='filter_arrival_time_min'
    )
    scheduled_arrival_time_range_max = django_filters.NumberFilter(
        method='filter_arrival_time_max'
    )
    status = django_filters.MultipleChoiceFilter(
        choices=[
            ("scheduled", "scheduled"),
            ("departed", "departed"),
            ("delayed", "delayed"),
            ("arrived", "arrived"),
            ("cancelled", "cancelled"),
        ],
        label="Flight Status",
    )

    class Meta:
        model = Flight
        fields = ['counterpart','counterpart_airport'   ]

    
    def filter_has_economy(self, queryset, name, value):
        if value:     
            return queryset.filter(Economy_Class_Num__gt=0)
        return queryset

    def filter_has_premium_economy(self, queryset, name, value):
        if value:
            return queryset.filter(Premium_Economy_Num__gt=0)
        return queryset

    def filter_has_business(self, queryset, name, value):
        if value:
            return queryset.filter(Business_Class_Num__gt=0)
        return queryset

    def filter_has_first_class(self, queryset, name, value):
        if value:
            return queryset.filter(First_Class_Num__gt=0)
        return queryset


    def filter_departure_time_min(self, queryset, name, value):
        return queryset.annotate(
            hour=ExtractHour('scheduled_departure')
        ).filter(hour__gte=value)


    def filter_departure_time_max(self, queryset, name, value):
        return queryset.annotate(
            hour=ExtractHour('scheduled_departure')
        ).filter(hour__lte=value)
    

    def filter_arrival_time_min(self, queryset, name, value):
        return queryset.annotate(
            hour=ExtractHour('scheduled_arrival')
        ).filter(hour__gte=value)


    def filter_arrival_time_max(self, queryset, name, value):
        return queryset.annotate(
            hour=ExtractHour('scheduled_arrival')
        ).filter(hour__lte=value)
    
