from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("account.urls")),
    path("", include("function.urls")),
    path("", include("portfolio.urls")),
    path("schedule/", include("schedule.urls")),
    path("memorize/", include("memorize.urls")),
    path('blog/', include('blog.urls')),
    path('imageblog/', include('imageblog.urls')),
    path('dialog/', include('dialog.urls')),
    path('summernote/', include('django_summernote.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
