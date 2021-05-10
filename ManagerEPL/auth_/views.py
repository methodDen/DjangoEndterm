import logging

from django.shortcuts import render
from rest_framework import generics, mixins, permissions, status
from auth_.models import MainUser, Profile
from auth_.serializers import MainUserSerializer, ProfileSerializer

logger = logging.getLogger(__name__)


# Create your views here.
class MainUsersListApiView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = MainUser.objects.all()
    serializer_class = MainUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProfileApiView(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Profile is updated: {serializer.instance}')

    def perform_destroy(self, instance):
        instance.delete()
        logger.warning(f'Profile is deleted, {instance}')
