from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketing_course',
            name='image',
            field=models.ImageField(upload_to='courses/images/'),
        ),
        migrations.AlterField(
            model_name='marketing_lecture',
            name='image',
            field=models.ImageField(upload_to='courses/images/'),
        ),
        migrations.AlterField(
            model_name='marketing_lecture',
            name='video',
            field=models.FileField(upload_to='courses/videos/'),
        ),
    ]
