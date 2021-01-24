import logging
from django.core.management.base import BaseCommand
from django.utils import timezone


from ...models import Table, GameSession

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates game sessions for the future."

    def handle(self, *args, **options):
        creation_time_start = timezone.now() + timezone.timedelta(days=28)
        days_to_add = 7

        try:
            table = Table.objects.get(name="Online")
        except Table.DoesNotExist:
            logger.warning(
                "There is no online table set!"
            )
            return

        for day in range(1, days_to_add+1):
            session_time = creation_time_start + timezone.timedelta(days=day)
            GameSession.objects.get_or_create(
                date=session_time.date(),
                table=table,
                active=True,
                spots=table.max_spots,
            )
