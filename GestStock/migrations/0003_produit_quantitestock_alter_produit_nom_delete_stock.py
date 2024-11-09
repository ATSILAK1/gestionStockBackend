# Generated by Django 5.0.1 on 2024-11-04 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestStock', '0002_fournisseur_remove_produit_fournisseur_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='quantiteStock',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produit',
            name='nom',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]