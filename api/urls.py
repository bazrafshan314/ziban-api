from django.urls import path
from rest_framework import routers
from .views import GetTokenView, UserRegisterAPIView, UserListAPIView, UserLoginView
from .views import ProductViewSet
from django.views.generic import TemplateView
from django.urls import include

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/register/", UserRegisterAPIView.as_view(), name="user_create"),
    path("users/login/", UserLoginView.as_view(), name="user_login"),
    path("users/token/", GetTokenView.as_view(), name="get_token"),
    path("", include(router.urls)),
    # path("swagger/", UserCreateAPIView.as_view(), name="user_create"),
    path(
        "swagger.json/",
        TemplateView.as_view(template_name="swagger.json"),
        name="openapi-schema",
    ),
    path(
        "doc/",
        TemplateView.as_view(
            template_name="swagger.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="redoc",
    ),
]
