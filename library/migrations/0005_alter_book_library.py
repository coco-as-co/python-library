# Generated by Django 4.1.5 on 2023-01-07 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_book_jacket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='library',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Library', to='library.library'),
        ),
    ]
