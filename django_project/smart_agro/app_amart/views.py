from django.shortcuts import render


def accueil(request):
    return render(request, 'app_amart/accueil.html')


def services(request):
    return render(request,'app_amart/services.html')

def about_us(request):
    return render(request, 'app_amart/about_us.html')

def contact_view(request):
    return render(request, 'app_amart/contact.html')

# app_amart/views.py
from django.shortcuts import render, redirect
from .models import Message
from django.contrib import messages as django_messages

def contact_submit_view(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message_contenu = request.POST.get('message')

        # Sauvegarder le message dans la base de données
        Message.objects.create(nom=nom, email=email, contenu=message_contenu)

        # Ajouter un message de succès pour l'utilisateur
        django_messages.success(request, "Merci pour votre message. Nous vous répondrons bientôt.")

        return redirect('contact')

    return render(request, 'app_amart/contact.html')



from django.shortcuts import render
from .models import Message

def messages_view(request):
    messages = Message.objects.all()
    return render(request, 'app_amart/messages.html', {'messages': messages})


# # app_amart/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Message, Response
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings

# def repondre_message_view(request, message_id):
#     message = get_object_or_404(Message, pk=message_id)

#     if request.method == 'POST':
#         contenu_reponse = request.POST.get('reponse')
#         Response.objects.create(message=message, contenu=contenu_reponse)
#         message.repondu = True
#         message.save()

#         # Envoi de l'e-mail de réponse
#         sujet = "Réponse à votre message sur Smart Agro"
#         message_email = f"Merci pour votre message. Voici notre réponse : \n\n{contenu_reponse}"
#         send_mail(sujet, message_email, settings.DEFAULT_FROM_EMAIL, [message.email])

#         messages.success(request, "Réponse envoyée avec succès et un e-mail a été envoyé à l'utilisateur.")

#         return redirect('messages')

#     return render(request, 'app_amart/repondre_message.html', {'message': message})


    
