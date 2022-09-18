from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    model = Category
    empty_value_display = "-пусто-"


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    model = Genre
    empty_value_display = "-пусто-"


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    model = Title
    list_display = (
        "pk",
        "name",
        "year",
        "description",
        "category",
    )
    search_fields = ("name",)
    list_filter = ("year", "category")
    filter_horizontal = ("genre",)
    list_editable = ("category",)
    empty_value_display = "-пусто-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = (
        "title",
        "text",
        "author",
        "score",
        "pub_date",
    )
    list_editable = ("score",)
    search_fields = ("text",)
    list_filter = (
        "title",
        "author",
        "score",
        "pub_date",
    )
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    model = Comment
    list_display = (
        "review",
        "text",
        "author",
        "pub_date",
    )
    search_fields = ("text",)
    list_filter = (
        "review_id",
        "author",
        "pub_date",
    )
    empty_value_display = "-пусто-"
