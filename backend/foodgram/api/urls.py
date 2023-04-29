from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientsViewSet, TagsViewSet, UserViewSet

router = SimpleRouter()

router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
