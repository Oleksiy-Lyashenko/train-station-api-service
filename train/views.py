from django.db.models import F, Count
from django.shortcuts import render
from rest_framework import viewsets

from train.models import Crew, TrainType, Train, Station, Route, Journey
from train.serializers import CrewSerializer, TrainTypeSerializer, TrainSerializer, StationSerializer, RouteSerializer, \
    RouteListSerializer, RouteDetailSerializer, JourneySerializer, JourneyListSerializer, JourneyDetailSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.select_related("train_type")
    serializer_class = TrainSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = (
        Journey.objects.all()
        .select_related(
            "route", "train"
        ).annotate(
            seats_available=(
                F("train__places_in_cargo") - Count("tickets")
            )
        )
    )
    serializer_class = JourneySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer

        if self.action == "retrieve":
            return JourneyDetailSerializer

        return JourneySerializer

