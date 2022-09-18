from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from api_yamdb.common.models import PubDateModel
from api_yamdb.users.models import User


class Category(models.Model):
    """Модель для категорий (типов) произведений."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров произведений."""

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Модель для произведений, к которым пишут рецензии
    (определённый фильм, книга или песня).
    """

    name = models.CharField(
        max_length=200, verbose_name="Название произведения"
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год создания",
        validators=[MaxValueValidator(limit_value=timezone.now().year)]
    )
    description = models.TextField(
        blank=True, verbose_name="Описание произведения"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория",
        help_text="Категория, к которой будет относиться произведение",
    )
    genre = models.ManyToManyField(
        Genre,
        through="TitleGenre",
        related_name="titles",
        verbose_name="Жанр",
        help_text="Жанры произведения",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель связей произведений (Titles) с жанрами (Genres)."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_relationships",
                fields=["title", "genre"],
            ),
        ]

    def __str__(self):
        return f"{self.title.name} - {self.genre.name}"


class Review(PubDateModel):
    """Модель для рецензий."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(
        verbose_name="Текст рецензии",
        help_text="Введите текст рецензии"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор"
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
        ordering = ("-pub_date",)

        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique review per title"
            )
        ]

    def __str__(self):
        return self.text


class Comment(PubDateModel):
    """Модель для комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Рецензия",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text="Введите текст комментария",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
