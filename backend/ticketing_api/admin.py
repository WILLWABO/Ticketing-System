from django.contrib import admin

from .models import *

# Register your models here. We register our models on the administration page
admin.site.register(Ticket)
admin.site.register(Administrateur)
admin.site.register(Technicien)
admin.site.register(Client)
admin.site.register(Probleme)
admin.site.register(Service)
admin.site.register(Utilisateur)
admin.site.register(Relancer)