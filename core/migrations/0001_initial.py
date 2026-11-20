from django.db import migrations


def dar_permisos_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    try:
        user = User.objects.get(username='apparedesaa')
        user.is_staff = True
        user.is_superuser = True
        user.save()

    except User.DoesNotExist:
        User.objects.create_superuser(
            'apparedesaa',
            'admin@utec.com',
            'Admin12345!'
        )


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(dar_permisos_admin),
    ]