from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ads.views import *

router = SimpleRouter()
router.register("ads", AdViewSet)
router.register("ads/(?P<ad_pk>[^/.]+)/comments", CommentViewSet)
urlpatterns = [
    path('ads/me/', UserAdsListView.as_view(), name='user_ads'),
    path('', include(router.urls)),
]

