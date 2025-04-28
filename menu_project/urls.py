from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from menu.views import (
    HomePageView,
    AboutPageView,
    MainMenuView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('main-menu/', MainMenuView.as_view(), name='main-menu'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
      settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
