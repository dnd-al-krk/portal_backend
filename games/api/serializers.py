from rest_framework import serializers

from profiles.api.serializers import PublicProfileSerializer, PublicPlayerCharacterSerializer
from ..models import Adventure, GameSession, GameSessionPlayerSignUp


class AdventureSerializer(serializers.ModelSerializer):
    title_display = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()

    class Meta:
        model = Adventure
        fields = ("id", "title", "season", "number", "tier", "type", "title_display")

    def get_title_display(self, adventure):
        return str(adventure)

    def get_tier(self, adventure):
        return adventure.get_tier_display()


class GameSessionPlayerSignUpSerializer(serializers.ModelSerializer):
    profile = PublicProfileSerializer(source="player", read_only=True)
    character = PublicPlayerCharacterSerializer()

    class Meta:
        model = GameSessionPlayerSignUp
        fields = ("profile", "character")


class GameSessionSerializer(serializers.ModelSerializer):
    table_name = serializers.CharField(source="table.name", read_only=True)
    table_extra_notes = serializers.CharField(source="table.extra_notes", read_only=True)
    report_notes = serializers.SerializerMethodField()
    dm = PublicProfileSerializer(read_only=True)
    players = GameSessionPlayerSignUpSerializer(many=True, source="gamesessionplayersignup_set", read_only=True)
    adventure = AdventureSerializer()
    time_start = serializers.SerializerMethodField()
    time_end = serializers.SerializerMethodField()
    max_spots = serializers.IntegerField(source="table.max_spots", read_only=True)

    class Meta:
        model = GameSession
        fields = (
            "id",
            "date",
            "table_name",
            "table_extra_notes",
            "report_notes",
            "adventure",
            "dm",
            "players",
            "time_start",
            "time_end",
            "notes",
            "spots",
            "max_spots",
            "ended",
            "reported",
        )

    def get_time_start(self, game):
        return game.time_start.strftime("%H:%M") if game.time_start else ""

    def get_time_end(self, game):
        return game.time_end.strftime("%H:%M") if game.time_end else ""

    def get_report_notes(self, game):
        if self.context["request"].user.profile != game.dm:
            return ""
        return game.report_notes


class GameSessionReportSerializer(serializers.ModelSerializer):
    players = serializers.ListField(child=serializers.IntegerField(min_value=1))

    class Meta:
        model = GameSession
        fields = ("players", "extra_players", "report_notes")

    def update(self, instance, validated_data):
        players = validated_data.get("players")
        extra_players = validated_data.get("extra_players", None)
        report_notes = validated_data.get("report_notes", None)
        GameSessionPlayerSignUp.objects.filter(game=instance).update(reported=False)
        GameSessionPlayerSignUp.objects.filter(player_id__in=players, game=instance).update(reported=True)
        instance.report(extra_players=extra_players, report_notes=report_notes)
        return instance


class GameSessionBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = ("id", "dm", "adventure", "time_start", "time_end", "spots", "notes")
