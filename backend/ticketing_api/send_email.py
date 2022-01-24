
from django.core.mail import send_mail


def send_email_user(destinataire):
    return send_mail(
        "Finalisation d'un ticket",
        "Nous sommes heureux de vous annoncer que votre problème a été résolu. Vous pouvez a présent utiliser votre service sans problème.",
        "franklinfrost14@gmail.com",
        [destinataire],
        fail_silently=False
    )


def send_email_technician(destinataire):
    return send_mail(
        "Relance d'un ticket",
        "Nous vous informons que l'un des ticket dont vous avez la charge a été relancé par l'utilisateur.\nVeuillez accedez et repondre a sa demande le plus tôt possible",
        "franklinfrost14@gmail.com",
        [destinataire],
        fail_silently=False
    )


def send_email_admin(destinataire):
    return send_mail(
        "Relance d'un ticket",
        "Nous vous informons que l'un des ticket dont vous avez la charge a été relancé par l'utilisateur.\nVeuillez attribuez ce ticket à un technicien afin de le traiter le plus tôt possible",
        "franklinfrost14@gmail.com",
        [destinataire],
        fail_silently=False
    )
