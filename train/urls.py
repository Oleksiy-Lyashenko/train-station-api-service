from django.urls import path, include
from rest_framework import routers

from train.views import (
    CrewViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    StationViewSet,
    RouteViewSet,
    JourneyViewSet
)

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("train_types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("journeys", JourneyViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "train"
