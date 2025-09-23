# Generated manually because Django is unavailable in this environment
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "landing_page",
            "0015_alter_userlandingpage_title_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="userlandingpage",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="userlandingpage",
            name="description_ar",
            field=models.TextField(
                blank=True, null=True, verbose_name="Arabic description"
            ),
        ),
    ]
