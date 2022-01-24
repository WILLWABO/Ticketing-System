# from django.core.files.storage import default_storage
from django.db import models
import uuid
from django.db.models.fields.files import ImageField
from django.utils import timezone

# Create your models here.
class Utilisateur(models.Model):
    ROLE = (
        ('Admin', 'Admin'),
        ('Utilisateur', 'Utilisateur'),
        ('Technicien', 'Technicien'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50, null=False)
    prenom = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False, unique=True)
    role = models.CharField(choices=ROLE, max_length=15, null=False)
    date_inscription= models.DateTimeField(auto_now_add=True, null=False)
    password = models.CharField(max_length=30, null=False)
   
    def __str__(self):
        return self.nom + " : " + self.role

class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, null=False)
    fonction = models.TextField(null=True)

    def __str__(self):
        return self.nom

class Client(Utilisateur):
    pass

class Administrateur(Utilisateur):
    pass

class Technicien(Utilisateur):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)

class Probleme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True)
    activate = models.BooleanField(default=False)
    uploadFile = models.FileField(blank=True, null=True, upload_to="Fichiers", verbose_name='Ajouter un fichier  ')
    uploadImage= ImageField(blank=True, null=True, upload_to="Images", verbose_name='Ajouter une image  ' )


    def __str__(self):
        return self.nom


class Ticket(models.Model):

    SOURCEDAMANDE= (
        ('-1', 'Téléphone'),
        ('0', 'E-mail'),
        ('1', 'Directe'),
        ('2', 'Manuscrite'),
        ('3', 'Autre'),
    )

    PRIORITY= (
        ('-1', 'Basse'),
        ('0', 'Très basse'),
        ('1', 'Moyenne'),
        ('2', 'Haute'),
        ('3', 'Très haute'),
        ('4', 'Majeure'),
    )
    URGENCE= (
        ('Tres haute', 'Très haute'),
        ('Haute', 'Haute'),
        ('Moyenne', 'Moyenne'),
        ('Basse', 'Basse'),
        ('Tres basse', 'Très basse'),
    )

    IMPACT= (
        ('Tres haut', 'Très haut'),
        ('Haut', 'Haut'),
        ('Moyen', 'Moyen'),
        ('Bas', 'Bas'),
        ('Tres bas', 'Très bas'),
    )

    STATE= (
        ('Nouveau', 'Nouveau'),                   # à la creation du ticket, aucune action n'est encore effectuée sur celui-ci
        ('Encourscas1', 'Attribué'),
        ('Encourscas2', 'En cours de traitement'),
        ('Résolu', 'Résolu'),                     # lorsqu'une solution est proposée
        ('Attente', 'En attente'),                # le technicien attend des informations supplémentaires de la part du demandeur. 
        ('Clos', 'Clos'),                         # lorsque le demandeur valide la solution
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description= models.TextField(null=True)
    probleme = models.ForeignKey(Probleme, on_delete=models.SET_NULL, null=True)
    date_creation= models.DateTimeField(auto_now_add=True, null=False)
    date_echeance = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    urgence =  models.CharField(max_length=50, choices=URGENCE, default="Moyenne")   # L'urgence indique l'importance donnée par le demandeur au ticket                
    priorite =  models.CharField(max_length=50, choices=PRIORITY, default="Moyenne")             
    impact =  models.CharField(max_length=50, choices=IMPACT, default="Moyen")             
    source =  models.CharField(max_length=50, choices=SOURCEDAMANDE, default="Directe")                 
    etat = models.CharField(choices=STATE, max_length=20, null=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=False)
    technicien = models.ForeignKey(Technicien, on_delete=models.PROTECT, null=True)
    admin = models.ForeignKey(Administrateur, on_delete=models.PROTECT, null=True, related_name='admin')
    deleted = models.BooleanField(default=False)
    admin_deleted = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, default=None, null=True, related_name='admin_deleted')
    uploadFile = models.FileField(blank=True, null=True, upload_to="Fichiers", verbose_name='ajouter un fichier')
    uploadImage= ImageField(blank=True, null=True, upload_to="Images", verbose_name='ajouter une image' )


    def __str__(self):
        return str(self.id)

class Relancer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, null=False)
    nombre_relance = models.IntegerField(default=1)

    def __str__(self):
        return str(self.date_created)

# en mettant on_delete=modele.CASCADE dans le champ ticket de la table relancer,
#on supprimerait la relance si le ticket est supprimé et supprimer une relance ne supprime pas du tout le ticket

# si on_delete=models.PROTECT on ne peut pas supprimer le ticket sans avoir supprimé tous 
# les objects qui y font référence( ici relancer)

# s'il est à SET_NULL cela signifie que la suppression d'un ticket ne supprime pas la relance,
#sauf que la relance ne reférencira plus le ticket supprimé mais null.

#L'utilisation de related_name vous permet de spécifier un nom plus simple ou plus 
# lisible pour obtenir la relation inverse. Dans ce cas
# admin = models.ForeignKey(Administrateur, on_delete=models.PROTECT, null=True, related_name='admin')
# l'appel serait alors Administrateur.admin.all().


# verbose_name est le nom qui apparaîtra lors du remplissage de ce champm du formulaire