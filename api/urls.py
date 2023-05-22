from django.urls import path
from .views import GetTokenView, UserCreateAPIView, UserListAPIView
from django.views.generic import TemplateView

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("users/token/", GetTokenView.as_view(), name="get_token"),
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
