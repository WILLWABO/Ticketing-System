from django.urls import path, include
from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r'utilisateur', views.UtilisateurViewSet)
routers.register(r'administrateur', views.AdministrateurViewSet)
routers.register(r'ticket', views.TicketViewSet)
routers.register(r'technicien', views.TechnicienViewSet)
routers.register(r'client', views.ClientViewSet)
routers.register(r'service', views.ServiceViewSet)
routers.register(r'probleme', views.ProblemeViewSet)
routers.register(r'relance', views.RelancerViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('login/', views.login),
    path('all-tickets/', views.get_tickets),
    path('new-tickets/', views.get_new_tickets),
    path('waiting-tickets/', views.get_waiting_tickets),
    path('finished-tickets/', views.get_finished_tickets),
    path('relanced-tickets/', views.get_relance_tickets),
    path('affect-tickets/', views.ticket_to_technician),
    path('admin-stats/', views.get_admin_stats),
    path('new-problems/', views.get_new_problems),
    path('update-problem/', views.update_problem),

    path('all-user-tickets/<str:id>/', views.get_user_tickets),
    path('waiting-user-tickets/<str:id>/', views.get_user_waiting_tickets),
    path('finished-user-tickets/<str:id>/', views.get_user_finished_tickets),
    path('relanced-user-tickets/<str:id>/', views.get_user_relance_tickets),
    path('user-stats/<str:id>/', views.get_user_stats),
    path('relancer-tickets/<str:id>/', views.relance_a_ticket),

    path('all-technician-tickets/<str:id>/', views.get_technician_tickets),
    path('waiting-technician-tickets/<str:id>/',
         views.get_technician_waiting_tickets),
    path('finished-technician-tickets/<str:id>/',
         views.get_technician_finished_tickets),
    path('relanced-technician-tickets/<str:id>/',
         views.get_technician_relance_tickets),
    path('technician-stats/<str:id>/', views.get_technician_stats),
    path('finalize-tickets/<str:id>/', views.finalize_ticket),
    path('check-password/<str:id>/', views.check_new_technician),
    path('update-password/', views.update_password),



    path('techniciens/', views.get_technicien),
]
