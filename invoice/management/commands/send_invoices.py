from django.core.management.base import BaseCommand, CommandError
from ...utils import send_invoices


class Command(BaseCommand):
    help = 'Send due invoices'

    def handle(self, *args, **options):
        send_invoices()
