from django.db import models


class Quote(models.Model):
    text = models.TextField("Treść cytatu", max_length=500)
    author = models.CharField("Autor", max_length=100, blank=True)
    created_at = models.DateTimeField("Dodano", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "cytat"
        verbose_name_plural = "cytaty"

    def __str__(self):
        author = self.author or "Anonim"
        return f"{self.text[:50]} — {author}"
