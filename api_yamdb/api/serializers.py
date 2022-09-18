from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class AuthSignupSerializer(serializers.ModelSerializer):
    """Сериализатор для процедуры регистрации пользователя."""

    class Meta:
        email = serializers.EmailField(min_length=6)
        fields = ("username", "email")
        model = User

    def validate_username(self, value):
        """Валидация имени пользователя."""
        if value.lower() == "me":
            raise serializers.ValidationError(f'Username "{value}" is deny!')
        return value


class TokenSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения токена."""

    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()
        del self.fields["password"]

    def validate(self, attrs):
        """Валидация получения токена."""
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return {
            "username": attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
            "token": str(self.get_token(user)),
        }

    @classmethod
    def get_token(cls, user):
        """Возвращает токен."""
        return cls.token_class.for_user(user)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        lookup_field = "username"


class UserOwnerSerializer(serializers.ModelSerializer):
    """Сериализатор для владельца экземпляра модели User."""

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id", "name", "year", "rating", "description", "genre", "category"
        )

    def get_rating(self, obj):
        """Возвращает рейтинг."""
        score = obj.reviews.all().aggregate(
            Avg("score")
        ).get("score__avg", 0.00)
        return round(score, 2) if score else None

    def validate_year(self, year):
        """Проверяем что год не больше текущего."""
        if year > timezone.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего"
            )
        return year


class TitlesSlugSerializer(TitlesSerializer):
    """Сериализатор для модели Post по slug"""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        """Валидация отзыва на произведение."""
        if self.context.get("request").method == "POST":
            author = self.context.get("request").user
            title = self.context.get("title")
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    "Вы уже оставляли рецензию на это произведение!"
                )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
