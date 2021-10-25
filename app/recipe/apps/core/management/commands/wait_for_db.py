import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Comando Django para pausar a execução
        até que o banco de dados esteja disponível"""

    def handle(self, *args, **options):
        self.stdout.write('Esperando pelo banco de dados...')
        db_connection = None

        while not db_connection:
            try:
                db_connection = connections['default']

            except OperationalError:
                self.stdout.write(
                    'Banco de dados não disponível, espere um segundo...'
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Banco de dados disponível'))
