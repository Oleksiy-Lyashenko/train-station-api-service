from django.db.models import F, Count
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from train.models import Crew, TrainType, Train, Station, Route, Journey, Order
from train.serializers import CrewSerializer, TrainTypeSerializer, TrainSerializer, StationSerializer, RouteSerializer, \
    RouteListSerializer, RouteDetailSerializer, JourneySerializer, JourneyListSerializer, JourneyDetailSerializer, \
    OrderSerializer, OrderListSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.select_related("train_type")
    serializer_class = TrainSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        cargo_num = self.request.query_params.get("cargo_num")
        train_type = self.request.query_params("train_type")

        queryset = self.queryset

        if cargo_num:
            cargo_nums_ids = self._params_to_ints(cargo_num)
            queryset = queryset.filter(cargo_num__in=cargo_nums_ids)

        if train_type:
            train_types_ids = self._params_to_ints(train_type)
            queryset = queryset.filter(train_type__id__in=train_types_ids)

        return queryset.distinct()


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

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("source")

        queryset = self.queryset

        if source:
            sources_ids = self._params_to_ints(source)
            queryset = queryset.filter(source__id__in=sources_ids)

        if destination:
            destinations_ids = self._params_to_ints(destination)
            queryset = queryset.filter(destination__id__in=destinations_ids)

        return queryset.distinct()


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

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        route = self.request.query_params.get("route")
        train = self.request.query_params.get("train")

        queryset = self.queryset

        if route:
            routes_ids = self._params_to_ints(route)
            queryset = queryset.filter(route__id__in=routes_ids)

        if train:
            trains_ids = self._params_to_ints(train)
            queryset = queryset.filter(train__id__in=trains_ids)

        return queryset.distinct()


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__journey__route",
                "tickets__journey__train",
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
