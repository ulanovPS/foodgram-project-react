from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet, UserViewSet

router = SimpleRouter()

router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
