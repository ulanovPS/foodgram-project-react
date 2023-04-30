from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, IngredientsViewSet, TagsViewSet, RecipesViewSet

router = SimpleRouter()

router.register(r'tags', TagsViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
]
