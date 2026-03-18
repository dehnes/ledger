from django.db import migrations


def seed_countries(apps, schema_editor):
    Country = apps.get_model("common", "Country")

    # Selection of core SEPA countries
    countries = [
        # name, iso2, iso3, is_eu
        ("Germany", "DE", "DEU", True),
        ("Austria", "AT", "AUT", True),
        ("France", "FR", "FRA", True),
        ("Italy", "IT", "ITA", True),
        ("Spain", "ES", "ESP", True),
        ("Netherlands", "NL", "NLD", True),
        ("Belgium", "BE", "BEL", True),
        ("Switzerland", "CH", "CHE", False),
        ("United Kingdom", "GB", "GBR", False),
        ("Norway", "NO", "NOR", False),
        ("Luxembourg", "LU", "LUX", True),
        ("Ireland", "IE", "IRL", True),
    ]

    for name, iso2, iso3, is_eu in countries:
        Country.objects.update_or_create(
            iso_code=iso2,
            defaults={"name": name, "iso_code_3": iso3, "is_eu_member": is_eu},
        )


def remove_countries(apps, schema_editor):
    Country = apps.get_model("common", "Country")
    Country.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0001_initial"),  # This must match your first migration
    ]

    operations = [
        migrations.RunPython(seed_countries, remove_countries),
    ]
