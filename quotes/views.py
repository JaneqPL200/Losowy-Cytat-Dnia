import random

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import QuoteForm
from .models import Quote

SESSION_KEY = "quote_of_day"


def _pick_random(exclude_id=None):
    ids = list(Quote.objects.values_list("id", flat=True))
    if not ids:
        return None
    if exclude_id in ids and len(ids) > 1:
        ids.remove(exclude_id)
    return Quote.objects.get(pk=random.choice(ids))


def random_quote(request):
    today = timezone.localdate().isoformat()
    stored = request.session.get(SESSION_KEY)
    quote = None

    if stored and stored.get("date") == today:
        quote = Quote.objects.filter(pk=stored.get("id")).first()

    if quote is None:
        quote = _pick_random()
        if quote is not None:
            request.session[SESSION_KEY] = {"id": quote.pk, "date": today}

    return render(request, "quotes/random_quote.html", {"quote": quote})


@require_POST
def reroll(request):
    stored = request.session.get(SESSION_KEY) or {}
    quote = _pick_random(exclude_id=stored.get("id"))

    if quote is None:
        messages.warning(request, "Brak cytatów w bazie – dodaj pierwszy!")
        return redirect("quotes:add")

    if Quote.objects.count() == 1:
        messages.info(request, "W bazie jest tylko jeden cytat – dodaj więcej, aby losowanie miało sens.")

    request.session[SESSION_KEY] = {"id": quote.pk, "date": timezone.localdate().isoformat()}
    return redirect("quotes:random")


def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cytat został dodany. Dziękujemy!")
            return redirect("quotes:add")
        messages.error(request, "Formularz zawiera błędy – popraw je i spróbuj ponownie.")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def csrf_failure(request, reason=""):
    return render(request, "403_csrf.html", {"reason": reason}, status=403)