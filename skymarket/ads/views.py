from rest_framework import pagination, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ads.models import Ad, Comment
from ads.permissions import IsOwner, IsAdmin
from ads.serializers import AdDetailSerializer, AdCreateSerializer, AdSerializer, CommentSerializer, \
    CommentCreateSerializer


class AdPagination(pagination.PageNumberPagination):
    pass

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()

    serializers = {
        'retrieve': AdDetailSerializer,
        'create': AdCreateSerializer,
    }
    default_serializer = AdSerializer

    permissions = {
        'create': [IsAuthenticated],
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner | IsAdmin],
    }
    default_permission = [AllowAny]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()


    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        return super().create(request, *args, **kwargs)


    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    serializers = {
        'create': CommentCreateSerializer,
    }
    default_serializer = CommentSerializer

    permissions = {
        'create': [IsAuthenticated],
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsOwner | IsAdmin],
    }
    default_permission = [AllowAny]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()


    def create(self, request, *args, **kwargs):
        ad_pk = self.kwargs.get('ad_pk')

        data = {
            'ad': ad_pk,
            'author': request.user.pk,
            'text': request.data.get('text')
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserAdsListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(author=request.user)

        return super().list(request, *args, **kwargs)