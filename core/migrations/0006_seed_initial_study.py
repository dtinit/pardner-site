"""
Data migration: seed initial Vertical, Service, and Study records.

Why this exists:
    The database schema (tables) is created by migrations 0001-0005, but those
    migrations only define *structure* — they insert no rows. Without at least
    one Study linked to a Service, the homepage is completely empty and the
    OAuth donation flow can never be triggered.

    This migration inserts the minimum set of records required for the site to
    be functional out-of-the-box in every environment (local, staging,
    production). Because it runs automatically during `manage.py migrate`, it
    is applied by the CI/CD pipeline before Cloud Run is deployed, so the
    production database is seeded without any manual steps.

What it creates:
    - Vertical  : name="feed post"    (Vertical.VerticalName.FEED_POST)
    - Service   : name="tumblr"        (Service.ServiceName.TUMBLR)
                  linked to the "feed post" vertical
    - Study     : "Social Media Feed Research"
                  linked to the "tumblr" service

Reversibility:
    The reverse function removes the three records created above so that
    `manage.py migrate core 0005` cleanly rolls back the seed data.
"""

from django.db import migrations


def seed_initial_study(apps, schema_editor):
    Vertical = apps.get_model("core", "Vertical")
    Service = apps.get_model("core", "Service")
    Study = apps.get_model("core", "Study")

    # Create the "feed post" vertical
    vertical, _ = Vertical.objects.get_or_create(name="feed post")

    # Create the "tumblr" service and link it to the "feed post" vertical
    service, _ = Service.objects.get_or_create(name="tumblr")
    service.verticals.add(vertical)

    # Create the seed study and link it to the tumblr service
    study, _ = Study.objects.get_or_create(
        name="Social Media Feed Research",
        defaults={
            "authors": "DTI Research Team",
            "description": (
                "A study collecting donated Tumblr feed post data to research "
                "social media content patterns."
            ),
        },
    )
    study.services.add(service)


def reverse_seed(apps, schema_editor):
    Vertical = apps.get_model("core", "Vertical")
    Service = apps.get_model("core", "Service")
    Study = apps.get_model("core", "Study")

    Study.objects.filter(name="Social Media Feed Research").delete()
    Service.objects.filter(name="tumblr").delete()
    Vertical.objects.filter(name="feed post").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_serviceaccount_completed_donation_at_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_initial_study, reverse_code=reverse_seed),
    ]
