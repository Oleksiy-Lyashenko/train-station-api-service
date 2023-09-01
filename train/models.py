from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class Crew(models.Model):
    first_name = models.CharField(max_length=83)
    last_name = models.CharField(max_length=83)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name"]


class TrainType(models.Model):
    name = models.CharField(max_length=83)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=83)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType,
        on_delete=models.CASCADE,
        related_name="trains"
    )

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Cargo number: {self.cargo_num}\n"
            f"Count of places: {self.places_in_cargo}\n"
            f"Train type: {self.train_type.name}"

        )

    class Meta:
        ordering = ["name"]


class Station(models.Model):
    name = models.CharField(max_length=83, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        null=True,
        related_name="source"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        null=True,
        related_name="destination"
    )
    distance = models.IntegerField()

    @property
    def name_of_full_way(self):
        return f"{self.source} - {self.destination}"

    def __str__(self):
        return f"Route: {self.source.name} - {self.destination.name}, distance: {self.distance}"

    class Meta:
        unique_together = ("source", "destination", "distance")
        ordering = ["-distance"]
        constraints = [
            UniqueConstraint(
                fields=["source", "destination", "distance"],
                name="unique_source_destination_distance")
        ]

    def clean(self):
        if self.source.name == self.destination.name:
            raise ValidationError(
                f"Source and destination names should be difference"
            )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Route, self).save(
            force_insert, force_update, using, update_fields
        )


class Journey(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="journeys"
    )
    train = models.ForeignKey(
        Train,
        on_delete=models.SET_NULL,
        null=True,
        related_name="journeys"
    )
    crew = models.ManyToManyField(
        Crew,
        related_name="journeys"
    )
    departure_time = models.DateTimeField(auto_now=False)
    arrival_time = models.DateTimeField(auto_now=False)

    def __str__(self):
        return f"{self.route.source.name} - {self.route.destination.name} in {self.departure_time}"

    class Meta:
        ordering = ["departure_time"]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(
        Journey,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ("cargo", "seat", "journey")
        ordering = ["seat"]
        constraints = [
            UniqueConstraint(
                fields=["cargo", "seat", "journey"],
                name="unique_cargo_seat_journey")
        ]

    def clean(self):
        if not (1 <= self.seat <= self.journey.train.places_in_cargo):
            raise ValidationError({
                "seat": f"Seat must be in range [1, {self.journey.train.places_in_cargo}]"
            })

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
