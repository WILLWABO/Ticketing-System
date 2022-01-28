
from rest_framework import serializers
from .models import *

class UtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'url',
            'nom',
            'prenom',
            'email',
            'role',
            'date_inscription',
            'password'
        ]

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket  
        fields = [
            'id',
            'url',
            'description',
            'probleme',
            'date_creation',
            'etat',
            'source',
            'service',
            'client',
            'technicien',
            'admin',
            'uploadFile',    
            'uploadImage'
        ]

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id',
            'url',
            'nom',
            'fonction'
        ]

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'url',
            'nom',
            'prenom',
            'email',
            'role',
            'date_inscription',
            'password'
        ]

class TechnicienSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Technicien
        fields = [
            'id',
            'url',
            'service',
            'nom',
            'prenom',
            'email',
            'role',
            'date_inscription',
            'password'
        ]

class AdministrateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Administrateur
        fields = [
            'id',
            'url',
            'nom',
            'prenom',
            'email',
            'role',
            'date_inscription',
            'password'
        ]

class ProblemeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Probleme
        fields = [
            'id',
            'url',
            'nom',
            'description',
            'priorite',
            'activate',
            'uploadFile',
            'uploadImage'
        ]

class RelancerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Relancer
        fields = [
            'id',
            'url',
            'date_created',
            'date_updated',
            'ticket',
            'nombre_relance'
        ]

