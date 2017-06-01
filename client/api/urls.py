from django.conf.urls import url
from .views import ClientListView, ClientUpdateView

urlpatterns = [
    url(r'^clients/$', ClientListView.as_view(), name='clients_list'),
    url(r'^clients/(?P<pk>\d+)$', ClientUpdateView.as_view(), name='clients_update'),
]
