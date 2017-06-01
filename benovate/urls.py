from django.conf.urls import url, include
from django.contrib import admin

from client.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^api/', include('client.api.urls', namespace="api")),
]
