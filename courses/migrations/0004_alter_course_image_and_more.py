from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_viewlecture_user_viewcourse_course_viewcourse_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='courses/images/'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='image',
            field=models.ImageField(upload_to='courses/images/'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='video',
            field=models.FileField(upload_to='courses/videos/'),
        ),
    ]
