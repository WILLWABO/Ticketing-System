from datetime import date
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from .send_email import send_email_technician, send_email_user, send_email_admin

# Create your views here.


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class AdministrateurViewSet(viewsets.ModelViewSet):
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurSerializer


class TechnicienViewSet(viewsets.ModelViewSet):
    queryset = Technicien.objects.all()
    serializer_class = TechnicienSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):

        try:
            serializer = ClientSerializer(
                data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            """ data = serializer.data[0]
            data.pop("date_inscription") """

            result = {
                "success": True,
                "message": "Client successfully created",
                "data": serializer.data
            }
            return Response(result, status=status.HTTP_201_CREATED)
        except:
            result = {
                "success": False,
                "message": "Client not created",
                "data": {}
            }
            return Response(result, status=status.HTTP_200_OK)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ProblemeViewSet(viewsets.ModelViewSet):
    queryset = Probleme.objects.all()
    serializer_class = ProblemeSerializer


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer


class RelancerViewSet(viewsets.ModelViewSet):
    queryset = Relancer.objects.all()
    serializer_class = RelancerSerializer


@api_view(['POST'])
def login(request):

    if (("email" not in request.data) or ("password" not in request.data)):
        result = {
            "success": False,
            "message": "Seul les champs 'email' et 'password' sont acceptés",
            "data": {}
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    if (request.method == 'POST'):
        email = request.data["email"]
        password = request.data["password"]

        user = None
        try:
            user = Utilisateur.objects.filter(email=email, password=password)

            serializer = UtilisateurSerializer(
                user, many=True, context={'request': request})

            data = serializer.data[0]
            data.pop("date_inscription")
            data.pop("password")

            result = {
                "success": True,
                "message": "La connexion s'est bien passée",
                "data": data
            }
            return Response(result, status=status.HTTP_200_OK)
        except:
            result = {
                "success": False,
                "message": "Vérifiez votre email et mot de passe",
                "data": {},
            }
            return Response(result, status=status.HTTP_200_OK)


def ticket_sub_getter(tickets: Ticket, request):
    serializer = TicketSerializer(
        tickets, many=True, context={'request': request})

    serializer_ticket = serializer.data
    for ticket in serializer_ticket:
        # modify service field
        service = ticket["service"]
        id = service[service.find('service')+7:]
        id = id.replace('/', '')

        service = Service.objects.get(id=id)
        serializer = ServiceSerializer(service, context={'request': request})
        ticket["service"] = serializer.data["nom"]

        # modify client field
        client = ticket["client"]
        id = client[client.find('client')+6:]
        id = id.replace('/', '')

        client = Client.objects.get(id=id)
        serializer = ClientSerializer(client, context={'request': request})
        ticket["client"] = serializer.data["nom"] + \
            " " + serializer.data["prenom"]

        # modify technician field
        tech = ticket["technicien"]
        if tech is None:
            ticket["technicien"] = "Aucun"
        else:
            id = tech[tech.find('technicien')+10:]
            id = id.replace('/', '')

            tech = Technicien.objects.get(id=id)
            ticket["technicien"] = tech.nom + " " + tech.prenom

        # get priority of ticket
        # problem = ticket["probleme"]

        # if problem is None:
        #     ticket["priorite"] = "Inconnu"
        # else:
        #     id = problem[problem.find('probleme')+8:]
        #     id = id.replace('/', '')

        #     switcher = {
        #         -1: 'Inconnu',
        #         0: 'Normal',
        #         1: 'Urgent',
        #         2: 'Critique'
        #     }

        #     problem = Probleme.objects.get(id=id)
        #     ticket["priorite"] = switcher.get(problem.priorite, "Inconnu")

        # ticket.pop('probleme')

        # arrange date format
        dates = ticket["date_creation"]
        dates = dates[: 19]
        dates = dates.replace('T', ' à ')
        ticket["date_creation"] = dates

        dates = ticket["date_echeance"]
        dates = dates[: 19]
        dates = dates.replace('T', ' à ')
        ticket["date_echeance"] = dates

    result = {
        "success": True,
        "message": "Opération éffectuée avec succès",
        "data": serializer_ticket
    }

    return result


def ticket_getter(tickets: Ticket, request):
    """
        Basic ticket function used by all other views based on collecting tickets.
        This function is used to limit code repetition
    """
    result = ticket_sub_getter(tickets=tickets, request=request)

    return Response(result, status=status.HTTP_200_OK)


""" ---------------------------------------------- ADMINISTRATOR ---------------------------------------------- """


@api_view(['GET'])
def get_technicien(request):

    technicien = Technicien.objects.all()
    serializer = TechnicienSerializer(
        technicien, many=True, context={'request': request})

    serializer_technicien = serializer.data
    for tech in serializer_technicien:
        # modify service field
        service = tech["service"]
        id = service[service.find('service')+7:]
        id = id.replace('/', '')

        service = Service.objects.get(id=id)
        serializer = ServiceSerializer(service, context={'request': request})
        tech["service"] = serializer.data["nom"]

        # count number of current tickets
        for t in technicien:
            if str(t.id) == tech["id"]:
                tickets = Ticket.objects.filter(
                    technicien=t).exclude(etat="Résolu")
                tech["number_ticket"] = len(tickets)
                break

        # arrange date format
        dates = tech["date_inscription"]
        dates = dates[: 19]
        dates = dates.replace('T', ' à ')
        tech["date_inscription"] = dates

    result = {
        "success": True,
        "message": "Opération éffectuée avec succès",
        "data": serializer_technicien
    }

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_tickets(request):
    """
        This view permits to get all the available tickets
    """

    tickets = Ticket.objects.filter(deleted=False).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_new_tickets(request):
    """
        This view permits to get new the tickets (tickets that haven't been allocated to a technician)
    """

    tickets = Ticket.objects.filter(
        technicien=None, deleted=False).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_waiting_tickets(request):
    """
        This view permits to get all waiting tickets (tickets that have been allocated to a technician)
    """

    tickets = Ticket.objects.filter(deleted=False, etat="En cours de traitement").exclude(
        technicien=None).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_finished_tickets(request):
    """
        This view permits to get all the finished tickets
    """

    tickets = Ticket.objects.filter(deleted=False, etat="Résolu").exclude(
        technicien=None).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_relance_tickets(request):
    """
        This view permits to get all the relanced tickets
    """

    tickets = Ticket.objects.filter(deleted=False).exclude(
        etat="Résolu").order_by('-date_creation')

    # get all relanced associated to a ticket
    relance = []
    ticket_relance = []  # contains all the tickets which have been relanced
    for tick in tickets:
        if len(Relancer.objects.filter(ticket=tick)) > 0:
            relance.append(Relancer.objects.get(ticket=tick))
            ticket_relance.append(tick)

    ticket_response = ticket_sub_getter(
        tickets=ticket_relance, request=request)  # serialize all relanced tickets

    # update data field in response so as to add relanced date and number of relance
    for data in ticket_response["data"]:
        for tick in relance:
            if str(tick.ticket.id) == data["id"]:
                # format date
                dates = str(tick.date_updated)
                dates = dates[: 19]

                data["date_created"] = dates
                data["nombre_relance"] = tick.nombre_relance
                break

    return Response(ticket_response, status=status.HTTP_200_OK)


@api_view(['POST'])
def ticket_to_technician(request):
    """
        This view permits an administrator to affect a ticket to a technician
    """

    if (("admin" not in request.data) or ("technicien" not in request.data) or ("ticket" not in request.data)):
        result = {
            "success": False,
            "message": "Seul les champs 'admin' et 'technicien' sont acceptés",
            "data": {}
        }
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    if (request.method == 'POST'):
        idAdmin = request.data["admin"]
        idTechnicien = request.data["technicien"]
        idTicket = request.data["ticket"]

        ticket = Ticket.objects.get(id=idTicket)
        technicien = Technicien.objects.get(id=idTechnicien)
        admin = Administrateur.objects.get(id=idAdmin)

        if ticket.technicien is None:
            result = {
                "success": True,
                "message": "Le ticket a été attribué avec success à un technicien",
            }
        else:
            result = {
                "success": True,
                "message": "Le technicien affecté au ticket a été changé avec success",
            }

        ticket.technicien = technicien
        ticket.admin = admin
        ticket.etat = "En cours de traitement"
        ticket.save()

        serializer = TicketSerializer(ticket, context={'request': request})
        result["data"] = serializer.data

        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_admin_stats(request):
    """
        This view is used to get admin stats on different tickets
    """
    result = {}
    num_wait_tik = len(Ticket.objects.filter(deleted=False, etat="En cours de traitement").exclude(
        technicien=None))

    num_new_tik = len(Ticket.objects.filter(
        technicien=None, deleted=False))

    num_rel_tik = len(Relancer.objects.all().exclude(ticket__etat="Résolu"))

    num_tech_tik = len(Technicien.objects.all())

    result["num_wait_tik"] = num_wait_tik
    result["num_new_tik"] = num_new_tik
    result["num_rel_tik"] = num_rel_tik
    result["num_tech_tik"] = num_tech_tik

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_new_problems(request):
    """
        This view permits admin to get new problem types created by the users
    """
    problemes = Probleme.objects.filter(priorite=-1)
    serializer = ProblemeSerializer(
        problemes, many=True, context={'request': request})

    result = {
        "status": True,
        "message": "Les aux problèmes ont été récupéré",
        "data": serializer.data
    }
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_problem(request):
    """
        This view permits admin to update a new problem types created by the users
    """

    try:
        problem = Probleme.objects.get(id=request.data["id"])
        problem.nom = request.data["nom"]
        problem.description = request.data["description"]
        problem.priorite = request.data["priorite"]
        problem.activate = True
        problem.save()

        serializer = ProblemeSerializer(problem, context={'request': request})
        result = {
            "success": True,
            "message": "Le problème a été mis à jour sans problème",
            "data": serializer.data
        }
        return Response(result, status=status.HTTP_200_OK)
    except:
        result = {
            "success": True,
            "message": "Une érreur est survenu",
            "data": {}
        }
        return Response(result, status=status.HTTP_200_OK)


""" ---------------------------------------------- CLIENT ---------------------------------------------- """


@api_view(['GET'])
def get_user_tickets(request, id):
    """
        This view permits to get all a user's available tickets
    """

    client = Client.objects.get(id=id)
    tickets = Ticket.objects.filter(
        deleted=False, client=client).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_user_waiting_tickets(request, id):
    """
        This view permits to get all waiting tickets of a user (tickets that have been allocated to a technician)
    """

    client = Client.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, client=client, etat="En cours de traitement").exclude(
        technicien=None).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_user_finished_tickets(request, id):
    """
        This view permits to get all the finished tickets of a user (tickets that have been allocated to a technician)
    """

    client = Client.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, client=client, etat="Résolu").exclude(
        technicien=None).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_user_relance_tickets(request, id):
    """
        This view permits to get all the relanced tickets of a user
    """

    client = Client.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, client=client).exclude(
        etat="Résolu").order_by('-date_creation')

    # get all relanced associated to a ticket
    relance = []
    ticket_relance = []  # contains all the tickets which have been relanced
    for tick in tickets:
        if len(Relancer.objects.filter(ticket=tick)) > 0:
            relance.append(Relancer.objects.get(ticket=tick))
            ticket_relance.append(tick)

    ticket_response = ticket_sub_getter(
        tickets=ticket_relance, request=request)  # serialize all relanced tickets

    # update data field in response so as to add relanced date and number of relance
    for data in ticket_response["data"]:
        for tick in relance:
            if str(tick.ticket.id) == data["id"]:
                # format date
                dates = str(tick.date_updated)
                dates = dates[: 19]

                data["date_created"] = dates
                data["nombre_relance"] = tick.nombre_relance
                break

    return Response(ticket_response, status=status.HTTP_200_OK)


@api_view(['GET'])
def relance_a_ticket(request, id):
    """
        This view permits a user to relance a given ticket
    """

    ticket = Ticket.objects.get(id=id)
    if ticket.etat == "Résolu":
        result = {
            "success": True,
            "message": "Le ticket est déjà résolu. Impossible de le relancer.",
            "data": {}
        }
        return Response(result, status=status.HTTP_200_OK)

    try:
        # verify if a relance with this particular ticket exists. If it exists, we just increment the number of relance, else we create a new
        relance = Relancer.objects.get(ticket=ticket)
        relance.nombre_relance = relance.nombre_relance + 1
        relance.save()

        serializer = RelancerSerializer(relance, context={'request': request})

        result = {
            "success": True,
            "message": "Le nombre de relance de ce ticket a été mis à jour",
            "data": serializer.data
        }
        if ticket.etat == "Nouveau":
            admin = Administrateur.objects.all()[0]
            print(send_email_admin(admin.email))
        else:
            print(send_email_technician(ticket.technicien.email))
        return Response(result, status=status.HTTP_200_OK)
    except:
        relance = Relancer(ticket=ticket)

        serializer = RelancerSerializer(relance, context={'request': request})

        result = {
            "success": True,
            "message": "La nouvelle relance a été crée avec succès",
            "data": serializer.data
        }
        relance.save()
        print(send_email_technician(ticket.technicien.email))
        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_stats(request, id):
    """
        This view is used to get admin stats on different tickets
    """
    result = {}
    client = Client.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, client=client)

    num_wait_tik = len(tickets.filter(etat="En cours de traitement"))

    num_fin_tik = len(tickets.filter(etat="Résolu"))

    num_rel_tik = len(Relancer.objects.all().exclude(
        ticket__etat="Résolu").filter(ticket__client=client))

    num_new_tik = len(tickets.filter(etat="Nouveau"))

    result["num_wait_tik"] = num_wait_tik
    result["num_new_tik"] = num_new_tik
    result["num_rel_tik"] = num_rel_tik
    result["num_fin_tik"] = num_fin_tik

    return Response(result, status=status.HTTP_200_OK)


""" ---------------------------------------------- TECHNICIAN ---------------------------------------------- """


@api_view(['GET'])
def get_technician_tickets(request, id):
    """
        This view permits to get all available tickets of a technician
    """

    technicien = Technicien.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, technicien=technicien).exclude(
        technicien=None).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_technician_waiting_tickets(request, id):
    """
        This view permits to get all waiting tickets of a technician (tickets that have been allocated to a technician)
    """

    technicien = Technicien.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, technicien=technicien, etat="En cours de traitement").exclude(
        technicien=None).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_technician_finished_tickets(request, id):
    """
        This view permits to get all the finished tickets of a technician (tickets that have been allocated to a technician)
    """

    technicien = Technicien.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, technicien=technicien, etat="Résolu").exclude(
        technicien=None).order_by('-date_creation')
    return ticket_getter(tickets=tickets, request=request)


@api_view(['GET'])
def get_technician_relance_tickets(request, id):
    """
        This view permits to get all the relanced tickets of a technician
    """

    technicien = Technicien.objects.get(id=id)
    tickets = Ticket.objects.filter(deleted=False, technicien=technicien).exclude(
        etat="Résolu").order_by('-date_creation')

    # get all relanced associated to a ticket
    relance = []
    ticket_relance = []  # contains all the tickets which have been relanced
    for tick in tickets:
        if len(Relancer.objects.filter(ticket=tick)) > 0:
            relance.append(Relancer.objects.get(ticket=tick))
            ticket_relance.append(tick)

    ticket_response = ticket_sub_getter(
        tickets=ticket_relance, request=request)  # serialize all relanced tickets

    # update data field in response so as to add relanced date and number of relance
    for data in ticket_response["data"]:
        for tick in relance:
            if str(tick.ticket.id) == data["id"]:
                # format date
                dates = str(tick.date_updated)
                dates = dates[: 19]

                data["date_created"] = dates
                data["nombre_relance"] = tick.nombre_relance
                break

    return Response(ticket_response, status=status.HTTP_200_OK)


@api_view(['GET'])
def finalize_ticket(request, id):
    """
        This view is use to finalize a ticket
    """
    ticket = Ticket.objects.get(id=id)
    if ticket.etat == 'Résolu':
        result = {
            "success": True,
            "message": "Le ticket avait déjà été résolu",
            "data": {}
        }
        return Response(result, status=status.HTTP_200_OK)

    ticket.etat = 'Résolu'
    ticket.save()

    result = {
        "success": True,
        "message": "La résolution du ticket a été éffectué",
        "data": {}
    }
    print(send_email_user(ticket.client.email))

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_technician_stats(request, id):
    """
        This view is used to get admin stats on different tickets
    """
    result = {}

    technicien = Technicien.objects.get(id=id)
    tickets = Ticket.objects.filter(
        deleted=False, technicien=technicien).exclude(technicien=None)

    num_wait_tik = len(tickets.filter(etat="En cours de traitement"))

    num_fin_tik = len(tickets.filter(etat="Résolu"))

    num_rel_tik = len(Relancer.objects.all().exclude(
        ticket__etat="Résolu").filter(ticket__technicien=technicien))

    result["num_wait_tik"] = num_wait_tik
    result["num_fin_tik"] = num_fin_tik
    result["num_rel_tik"] = num_rel_tik

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def check_new_technician(request, id):
    """
        This view permits a new technician to update his password
    """
    try:
        technicien = Technicien.objects.get(id=id)
        if technicien.password == "1234":
            update = True
        else:
            update = False

        result = {
            "status": True,
            "update": update
        }
        return Response(result, status=status.HTTP_200_OK)
    except:
        result = {
            "status": False
        }
        return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_password(request):
    """
        This view permits a new technician to update his password
    """
    try:
        technicien = Technicien.objects.get(id=request.data["id"])
        technicien.password = request.data["password"]
        technicien.save()

        result = {
            "status": True
        }
        return Response(result, status=status.HTTP_200_OK)
    except:
        result = {
            "status": False
        }
        return Response(result, status=status.HTTP_200_OK)


def root(request):
    return redirect('api/')



def nouveau_contact(request):
    sauvegarde = False

    if request.method == "POST":
        form = NouveauContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = Ticket()
            contact.nom = form.cleaned_data["nom"]
            contact.adresse = form.cleaned_data["adresse"]
            contact.photo = form.cleaned_data["photo"]
            contact.save()

            sauvegarde = True
    else:
        form = NouveauContactForm()

    return render(request, 'contact.html', locals())

def voir_contacts(request):
    contacts = Ticket.objects.all()
    return render(request, 'voir_contacts.html',{'contacts':contacts})
