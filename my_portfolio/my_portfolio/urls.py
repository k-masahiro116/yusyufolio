"""my_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #accountのurls.pyを読み込み
    path("account/", include("account.urls")),
    #functionのurls.pyを読み込み
    path("", include("function.urls")),
    #portfolioのurls.pyを読み込み
    path("", include("portfolio.urls")),
    #graphのurls.pyを読み込み
    path("", include("graph.urls")),
    #realtime_graphのurls.pyを読み込み
    path("", include("realtime_graph.urls")),
    path("chat/", include("chat.urls")),
    path("schedule/", include("schedule.urls")),
    path("tokenizer/", include("tokenizer.urls")),
    path("memorize/", include("memorize.urls")),
    path('blog/', include('blog.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
