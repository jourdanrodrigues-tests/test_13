from django.contrib.staticfiles.management.commands import (
    runserver,  # It plugs the static url when DEBUG is True
)
from django.core.management import call_command


class Command(runserver.Command):
    def add_arguments(self, parser):
        parser.add_argument(
            "--migrate",
            action="store_true",
            help="Migrate database before turning the server on.",
        )

        return super().add_arguments(parser)

    def handle(self, *args, **options):
        if options["migrate"]:
            call_command("migrate")

        return super().handle(*args, **options)
