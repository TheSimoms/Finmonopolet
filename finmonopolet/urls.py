"""finmonopolet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include

from finmonopolet import settings
from finmonopolet.api import SharedAPIRootRouter


def api_urls():
    from importlib import import_module

    for app in settings.INSTALLED_APPS:
        try:
            import_module(app + '.api')
        except (ImportError, AttributeError):
            pass

    return SharedAPIRootRouter.shared_router.urls


urlpatterns = [
    url(r'^api/', include(api_urls())),
]
