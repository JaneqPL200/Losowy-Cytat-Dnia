from django.core.management.base import BaseCommand

from quotes.models import Quote

SAMPLE = [
    ("Wiem, że nic nie wiem.", "Sokrates"),
    ("Myślę, więc jestem.", "René Descartes"),
    ("Nie ma drogi do szczęścia, szczęście jest drogą.", "Budda"),
    ("Człowiek jest tym, co robi z tego, co zrobiono z niego.", "Jean-Paul Sartre"),
    ("Początek jest najważniejszą częścią pracy.", "Platon"),
]


class Command(BaseCommand):
    help = "Dodaje przykładowe cytaty do bazy (pomija już istniejące)."

    def handle(self, *args, **options):
        created = 0
        for text, author in SAMPLE:
            _, was_created = Quote.objects.get_or_create(text=text, author=author)
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"Dodano {created} nowych cytatów."))
