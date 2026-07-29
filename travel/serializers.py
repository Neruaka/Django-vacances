from rest_framework import serializers

from .models import Destination, TravelWish


class DestinationSerializer(serializers.ModelSerializer):
    """
    Serialiseur public des destinations.
    wish_count est un champ CALCULE (lecture seule) : le client ne peut
    jamais l'envoyer, il est derive du nombre de TravelWish lies.
    """

    wish_count = serializers.IntegerField(source="wishes.count", read_only=True)

    class Meta:
        model = Destination
        fields = [
            "id",
            "city",
            "country",
            "continent",
            "description",
            "best_period",
            "average_budget",
            "wish_count",
            "created_at",
        ]
        read_only_fields = ["id", "wish_count", "created_at"]

    def validate_average_budget(self, value):
        """Validation metier : un budget moyen doit etre strictement positif."""
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "le budget moyen doit etre superieur a zero."
            )
        return value


class TravelWishSerializer(serializers.ModelSerializer):
    """
    Serialiseur des envies de voyage. 'user' est en lecture seule cote client :
    c'est le ViewSet (perform_create) qui l'attribue automatiquement depuis
    l'utilisateur authentifie, jamais depuis les donnees envoyees par le client.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    destination_name = serializers.CharField(
        source="destination.__str__", read_only=True
    )

    class Meta:
        model = TravelWish
        fields = [
            "id",
            "user",
            "username",
            "destination",
            "destination_name",
            "priority",
            "desired_period",
            "notes",
            "visited",
            "created_at",
        ]
        read_only_fields = ["id", "user", "username", "destination_name", "created_at"]

    def validate(self, data):
        """
        Validation metier : un utilisateur ne peut pas ajouter deux fois
        la meme destination a ses envies. La contrainte UniqueConstraint en
        base protege deja contre ce cas, mais cette validation renvoie un
        message d'erreur clair et exploitable par le client, plutot qu'une
        erreur technique liee a la base de donnees.
        """
        request = self.context.get("request")
        destination = data.get("destination")

        if not request or not request.user.is_authenticated:
            return data

        queryset = TravelWish.objects.filter(
            user=request.user,
            destination=destination,
        )

        # En cas de modification (PATCH/PUT), on exclut l'objet courant
        # de la verification, sinon il se detecterait lui-meme en doublon.
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                {"destination": "vous avez deja ajoute cette destination a vos envies."}
            )

        return data
