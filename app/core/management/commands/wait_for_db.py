import time
from typing import Any, Optional

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write(_('\nWaiting for database >>>'))
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(_('Database unavailable, waiting 1 second...'))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS(_('Database available!')))
