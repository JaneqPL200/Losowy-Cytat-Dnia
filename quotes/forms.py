from django import forms

from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "author"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "maxlength": 500,
                    "placeholder": "Wpisz treść cytatu…",
                }
            ),
            "author": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": 100,
                    "placeholder": "np. Sokrates (opcjonalnie)",
                }
            ),
        }
        error_messages = {
            "text": {
                "required": "Treść cytatu jest wymagana.",
                "max_length": "Cytat może mieć maksymalnie 500 znaków.",
            },
            "author": {"max_length": "Imię autora może mieć maksymalnie 100 znaków."},
        }

    def clean_text(self):
        text = " ".join(self.cleaned_data["text"].split())
        if len(text) < 5:
            raise forms.ValidationError("Cytat jest za krótki (minimum 5 znaków).")
        return text

    def clean_author(self):
        return " ".join(self.cleaned_data.get("author", "").split())

    def clean(self):
        cleaned = super().clean()
        text = cleaned.get("text")
        author = cleaned.get("author", "")
        if text and Quote.objects.filter(text__iexact=text, author__iexact=author).exists():
            raise forms.ValidationError("Taki cytat już istnieje w bazie.")
        return cleaned

    def full_clean(self):
        super().full_clean()
        for name in self.errors:
            if name in self.fields:
                css = self.fields[name].widget.attrs.get("class", "")
                self.fields[name].widget.attrs["class"] = f"{css} is-invalid".strip()
