"""pydbug URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

from accounts.views import Profile, HandlerPage
from pydbug.routers import DefaultRouter
from ticket.urls import router as ticket_router

router = DefaultRouter()
router.extend(ticket_router)



urlpatterns = [
    path('', Profile.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('ticket/', include('ticket.urls')),
    path('api/', include(router.urls)),
    path('invitations/', include('invitations.urls', namespace='invitations')),
    path('handler/<str:code>/', HandlerPage.as_view(), name="handler")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
