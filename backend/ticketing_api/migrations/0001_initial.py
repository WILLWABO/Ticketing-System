# Generated by Django 3.1.4 on 2022-01-24 17:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Probleme',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('activate', models.BooleanField(default=False)),
                ('uploadFile', models.FileField(blank=True, null=True, upload_to='Fichiers', verbose_name='Ajouter un fichier  ')),
                ('uploadImage', models.ImageField(blank=True, null=True, upload_to='Images', verbose_name='Ajouter une image  ')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('fonction', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Utilisateur', 'Utilisateur'), ('Technicien', 'Technicien')], max_length=15)),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ticketing_api.utilisateur')),
            ],
            bases=('ticketing_api.utilisateur',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ticketing_api.utilisateur')),
            ],
            bases=('ticketing_api.utilisateur',),
        ),
        migrations.CreateModel(
            name='Technicien',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ticketing_api.utilisateur')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticketing_api.service')),
            ],
            bases=('ticketing_api.utilisateur',),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_echeance', models.DateTimeField(auto_now_add=True, null=True)),
                ('urgence', models.CharField(choices=[('Tres haute', 'Très haute'), ('Haute', 'Haute'), ('Moyenne', 'Moyenne'), ('Basse', 'Basse'), ('Tres basse', 'Très basse')], default='Moyenne', max_length=50)),
                ('priorite', models.CharField(choices=[('-1', 'Basse'), ('0', 'Très basse'), ('1', 'Moyenne'), ('2', 'Haute'), ('3', 'Très haute'), ('4', 'Majeure')], default='Moyenne', max_length=50)),
                ('impact', models.CharField(choices=[('Tres haut', 'Très haut'), ('Haut', 'Haut'), ('Moyen', 'Moyen'), ('Bas', 'Bas'), ('Tres bas', 'Très bas')], default='Moyen', max_length=50)),
                ('source', models.CharField(choices=[('-1', 'Téléphone'), ('0', 'E-mail'), ('1', 'Directe'), ('2', 'Manuscrite'), ('3', 'Autre')], default='Directe', max_length=50)),
                ('etat', models.CharField(choices=[('Nouveau', 'Nouveau'), ('Encourscas1', 'Attribué'), ('Encourscas2', 'En cours de traitement'), ('Résolu', 'Résolu'), ('Attente', 'En attente'), ('Clos', 'Clos')], max_length=20)),
                ('deleted', models.BooleanField(default=False)),
                ('uploadFile', models.FileField(blank=True, null=True, upload_to='Fichiers', verbose_name='ajouter un fichier')),
                ('uploadImage', models.ImageField(blank=True, null=True, upload_to='Images', verbose_name='ajouter une image')),
                ('probleme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ticketing_api.probleme')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing_api.service')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='admin', to='ticketing_api.administrateur')),
                ('admin_deleted', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_deleted', to='ticketing_api.administrateur')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing_api.client')),
                ('technicien', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ticketing_api.technicien')),
            ],
        ),
        migrations.CreateModel(
            name='Relancer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('nombre_relance', models.IntegerField(default=1)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing_api.ticket')),
            ],
        ),
    ]