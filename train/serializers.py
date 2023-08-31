from rest_framework import serializers

from train.models import Crew, TrainType, Train, Station, Journey, Route


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
            "crew"
        )


