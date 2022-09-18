from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyModelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `create()`, `destroy()`
    and `list()` actions.
    """

    pass
