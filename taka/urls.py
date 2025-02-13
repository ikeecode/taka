"""
URL configuration for taka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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


from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from media import views as media_views
from stories import views as stories_views

schema_view = get_schema_view(
   openapi.Info(
      title="PIKELO API",
      default_version='001',
      description="Pikélo API for BEN",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ikeecode@gmail.com"),
      license=openapi.License(name="MEST@africa License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', media_views.home),
    path('media/photos/<str:topic>', media_views.photos),
    path('media/populars/', media_views.populars, name='populars'),
    path('media/populars/<int:page_number>', media_views.next_page),
    path('stories/<str:type>/', stories_views.story_from_image),
     # documentation
    path('docs/', include([
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

