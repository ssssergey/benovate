from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView

from client.models import Client
from .serializers import ClientListSerializer, ClientUpdateSerializer


class ClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientListSerializer


class ClientUpdateView(UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.context['custom_response'])