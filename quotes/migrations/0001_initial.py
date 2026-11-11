from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Quote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(max_length=500, verbose_name="Treść cytatu")),
                ("author", models.CharField(blank=True, max_length=100, verbose_name="Autor")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Dodano")),
            ],
            options={
                "verbose_name": "cytat",
                "verbose_name_plural": "cytaty",
                "ordering": ["-created_at"],
            },
        ),
    ]
