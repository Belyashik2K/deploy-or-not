"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.http import (
    HttpRequest,
    JsonResponse,
)
from django.urls import path
from django.views.generic import RedirectView
from dmr.openapi import build_schema
from dmr.openapi.views import (
    OpenAPIJsonView,
    SwaggerView,
)
from dmr.routing import Router

from api.views import DecideController
from config.openapi import openapi_config


def handler404(request: HttpRequest, exception: Exception) -> JsonResponse:
    return JsonResponse(
        {
            "detail": "Not found. OpenAPI docs are available at /docs and /docs/openapi.json",
        },
        status=404,
    )


router = Router(
    "api/v1/",
    [
        path("decide", DecideController.as_view(), name="decide"),
    ],
)

schema = build_schema(router, config=openapi_config)

urlpatterns = [
    router.to_urlpatterns(namespace="api"),
    path("", RedirectView.as_view(pattern_name="swagger"), name="index"),
    path("docs/openapi.json/", OpenAPIJsonView.as_view(schema=schema), name="openapi-json"),
    path("docs/", SwaggerView.as_view(schema=schema), name="swagger"),
]
