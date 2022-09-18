from django_filters import CharFilter, FilterSet, ModelChoiceFilter

from reviews.models import Category, Genre, Title


class TitleFilter(FilterSet):
    category = ModelChoiceFilter(
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    genre = ModelChoiceFilter(
        to_field_name='slug',
        queryset=Genre.objects.all()
    )
    name = CharFilter(
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('year',)
