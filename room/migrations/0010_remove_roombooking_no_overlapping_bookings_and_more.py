# Generated by Django 4.2.1 on 2023-06-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0009_remove_roombooking_no_overlapping_bookings_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="roombooking",
            name="no_overlapping_bookings",
        ),
        migrations.AddConstraint(
            model_name="roombooking",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("end__gt", models.F("start")), ("start__lt", models.F("end"))
                    ),
                    models.Q(
                        ("end__lte", models.F("end")), ("start__gte", models.F("start"))
                    ),
                    models.Q(
                        ("end__gte", models.F("end")), ("start__lte", models.F("start"))
                    ),
                    _connector="OR",
                    _negated=True,
                ),
                name="no_overlapping_bookings",
            ),
        ),
    ]
