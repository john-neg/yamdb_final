from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from reviews.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title
from users.exceptions import ConfirmationCodeIsIncorrectError, UserNotFound
from users.models import User

from .permissions import IsAdminOrSuperUser, IsOwnerOrModeratorOrAdmin
from .serializers import (AuthSignupSerializer, CategoriesSerializer,
                          CommentsSerializer, GenresSerializer,
                          ReviewsSerializer, TitlesSerializer,
                          TitlesSlugSerializer, TokenSerializer,
                          UserSerializer)
from .viewsets import ListCreateDestroyModelViewSet


@api_view(["POST"])
def auth_signup(request):
    """Регистрация пользователя."""
    serializer = AuthSignupSerializer(data=request.data)
    if serializer.is_valid():
        user_instance = serializer.save(
            confirmation_code=User.objects.make_random_password(),
        )
        user_instance.send_confirmation_code()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def auth_token(request):
    """Получение токена."""
    serializer = TokenSerializer(data=request.data)
    try:
        if serializer.is_valid():
            return Response(
                {"token": serializer.validated_data.get("token")},
                status=status.HTTP_200_OK,
            )
    except ConfirmationCodeIsIncorrectError:
        raise ParseError
    except UserNotFound:
        raise NotFound
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """View класс для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = "username"

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(IsOwnerOrModeratorOrAdmin,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == "GET":
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            instance=user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.user.is_superuser or request.user.is_staff:
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyModelViewSet):
    """View класс для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            return (IsAdminOrSuperUser(),)
        return super().get_permissions()


class GenreViewSet(CategoryViewSet):
    """View класс для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """View класс для модели Title."""

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return (IsAuthenticatedOrReadOnly(),)
        return (IsAdminOrSuperUser(),)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitlesSerializer
        return TitlesSlugSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """View класс для модели Review."""

    serializer_class = ReviewsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["title"] = self.kwargs["title_id"]
        return context

    def get_permissions(self):
        if self.action in ("partial_update", "update", "destroy"):
            return (IsOwnerOrModeratorOrAdmin(),)
        return (IsAuthenticatedOrReadOnly(),)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """View класс для модели Comment."""

    serializer_class = CommentsSerializer

    def get_permissions(self):
        if self.action in ("partial_update", "update", "destroy"):
            return (IsOwnerOrModeratorOrAdmin(),)
        return (IsAuthenticatedOrReadOnly(),)

    def get_reviews(self):
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_reviews().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_reviews(), author=self.request.user)
