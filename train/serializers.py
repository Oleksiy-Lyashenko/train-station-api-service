from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from train.models import Crew, TrainType, Train, Station, Journey, Route, Ticket, Order


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    train_type = serializers.CharField(
        source="train_type.name", read_only=True
    )

    class Meta:
        model = Train
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id",)


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(serializers.ModelSerializer):
    source = RouteSerializer(many=True, read_only=True)
    destination = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = "__all__"


class JourneyListSerializer(serializers.ModelSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    train = TrainSerializer(many=False, read_only=True)
    seats_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "seats_available",
            "departure_time",
            "arrival_time",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["cargo", "seat", "journey"]
            )
        ]


class JourneyDetailSerializer(JourneySerializer):
    source = serializers.CharField(source="route.source.name", read_only=True)
    destination = serializers.CharField(source="route.destination.name", read_only=True)
    train_name = serializers.CharField(source="train.name", read_only=True)
    cargo_num = serializers.IntegerField(source="train.cargo_num", read_only=True)
    seats_available = serializers.IntegerField(read_only=True)
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    taken_seats = serializers.SlugRelatedField(
        source="tickets",
        many=True,
        read_only=True,
        slug_field="seat"
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "source",
            "destination",
            "departure_time",
            "arrival_time",
            "train_name",
            "cargo_num",
            "seats_available",
            "crew",
            "taken_seats"
        )


class TicketListSerializer(TicketSerializer):
    journey = JourneyListSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

