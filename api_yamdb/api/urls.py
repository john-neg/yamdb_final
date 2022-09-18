from django.urls import include, path
from rest_framework import routers

from api_yamdb.api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                                 ReviewViewSet, TitleViewSet, UsersViewSet,
                                 auth_signup, auth_token)

router_v1 = routers.DefaultRouter()
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register("users", UsersViewSet, basename="users")

auth_urls = [
    path("signup/", auth_signup, name="signup"),
    path("token/", auth_token, name="token"),
]

urlpatterns = [
    path("v1/auth/", include(auth_urls)),
    path("v1/", include(router_v1.urls)),
]
