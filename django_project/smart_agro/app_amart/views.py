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


    

    

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):  # Main screen
    return render(request, "app_amart/accueil.html", {'section': 'accueil'})



from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            
            new_user = user_form.save(commit=False)
            
            new_user.set_password(user_form.cleaned_data['password'])
            
            new_user.save()
            return render(request, 'app_amart/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'app_amart/register.html', {'user_form': user_form})



from django.contrib.auth.views import LogoutView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        next_page = reverse('login')  # Replace 'login' with the name of your login URL
        return HttpResponseRedirect(next_page)




# # prediction/views.py

# from django.shortcuts import render
# from .models import CropModel
# from .forms import CropPredictionForm

# def predict_crop(request):
#     model = CropModel()

#     if request.method == 'POST':
#         form = CropPredictionForm(request.POST)

#         if form.is_valid():
#             nitrogen = form.cleaned_data['Nitrogen']
#             phosphorus = form.cleaned_data['Phosphorus']
#             potassium = form.cleaned_data['Potassium']
#             temperature = form.cleaned_data['Temperature']
#             humidity = form.cleaned_data['Humidity']
#             ph = form.cleaned_data['Ph']
#             rainfall = form.cleaned_data['Rainfall']

#             result = model.predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)

#             return render(request, 'app_amart/predict.html', {'result': result, 'form': form})
#     else:
#         form = CropPredictionForm()

#     return render(request, 'app_amart/predict.html', {'form': form})

   






# prediction/views.py

from django.shortcuts import render
from .models import CropModel
from .forms import CropPredictionForm

def predict_crop(request):
    model = CropModel()

    if request.method == 'POST':
        form = CropPredictionForm(request.POST)

        if form.is_valid():
            nitrogen = form.cleaned_data['Nitrogen']
            phosphorus = form.cleaned_data['Phosphorus']
            potassium = form.cleaned_data['Potassium']
            temperature = form.cleaned_data['Temperature']
            humidity = form.cleaned_data['Humidity']
            ph = form.cleaned_data['Ph']
            rainfall = form.cleaned_data['Rainfall']

            result_label = model.predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
            
            # Map the numeric label to the corresponding crop name
            crop_dict = {
                1: 'Riz',
                2: 'Maïs',
                3: 'Haricots papillon',
                4: 'Haricot mungo',
                5: 'Haricot noir',
                6: 'Lentille',
                7: 'Banane',
                8: 'Mangue',
                9: 'Raisins',
                10: 'Pastèque',
                11: 'Melon miel',
                12: 'Pomme',
                13: 'Orange',
                14: 'Papaye',
                15: 'Café',
            }
            
            result_crop = crop_dict.get(result_label, "Unknown Crop")

            return render(request, 'app_amart/predict.html', {'result': (result_label, result_crop), 'form': form})
    else:
        form = CropPredictionForm()

    return render(request, 'app_amart/predict.html', {'form': form})


from django.shortcuts import render
import requests

def weather_view(request):
    cities = ['Akjoujt', 'Nouakchott', 'Nema', 'Aleg', 'Rosso', 'Barkewol', 'Kiffa', 'Tidjikia', 'BOUTILIMIT']
    selected_city = None
    
    if request.method == 'POST':
        selected_city = request.POST.get('city')
    
    if selected_city:
        current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
        api_key = "f4754342d786eef7ba4b60d2f3131e01"

        params = {
            "q": selected_city,
            "appid": api_key,
            "units": "metric"
        }

        response = requests.get(current_weather_url, params=params)

        if response.status_code == 200:
            weather_data = response.json()
            return render(request, 'weather.html', {'weather_data': weather_data, 'cities': cities, 'selected_city': selected_city})
        else:
            error_message = "La requête a échoué avec le code d'erreur: " + str(response.status_code)
            return render(request, 'error.html', {'error_message': error_message})
    else:
        # No city selected, render the form without weather data
        return render(request, 'weather.html', {'cities': cities})





import requests
import math
# from .models import Social

# Create your views here.

def index(request):
    return render(request, "app_amart/weather1.html")




def result(request):
    if request.method == "POST":
        city_name = request.POST["city"].lower()
        
        api_key = "f4754342d786eef7ba4b60d2f3131e01"  # Provide your OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"
        w_dataset = requests.get(url).json()
        try:
            context = {
                ####
                "city_name":w_dataset["city"]["name"],
                "city_country":w_dataset["city"]["country"],
                "wind":w_dataset['list'][0]['wind']['speed'],
                "degree":w_dataset['list'][0]['wind']['deg'],
                "status":w_dataset['list'][0]['weather'][0]['description'],
                "cloud":w_dataset['list'][0]['clouds']['all'],
                'date':w_dataset['list'][0]["dt_txt"],
                'date1':w_dataset['list'][1]["dt_txt"],
                'date2':w_dataset['list'][2]["dt_txt"],
                'date3':w_dataset['list'][3]["dt_txt"],
                'date4':w_dataset['list'][4]["dt_txt"],
                'date5':w_dataset['list'][5]["dt_txt"],
                'date6':w_dataset['list'][6]["dt_txt"],


                "temp": round(w_dataset["list"][0]["main"]["temp"] -273.0),
                "temp_min1":math.floor(w_dataset["list"][1]["main"]["temp_min"] -273.0),
                "temp_max1": math.ceil(w_dataset["list"][1]["main"]["temp_max"] -273.0),
                "temp_min2":math.floor(w_dataset["list"][2]["main"]["temp_min"] -273.0),
                "temp_max2": math.ceil(w_dataset["list"][2]["main"]["temp_max"] -273.0),
                "temp_min3":math.floor(w_dataset["list"][3]["main"]["temp_min"] -273.0),
                "temp_max3": math.ceil(w_dataset["list"][3]["main"]["temp_max"] -273.0),
                "temp_min4":math.floor(w_dataset["list"][4]["main"]["temp_min"] -273.0),
                "temp_max4": math.ceil(w_dataset["list"][4]["main"]["temp_max"] -273.0),
                "temp_min5":math.floor(w_dataset["list"][5]["main"]["temp_min"] -273.0),
                "temp_max5": math.ceil(w_dataset["list"][5]["main"]["temp_max"] -273.0),
                "temp_min6":math.floor(w_dataset["list"][6]["main"]["temp_min"] -273.0),
                "temp_max6": math.ceil(w_dataset["list"][6]["main"]["temp_max"] -273.0),


                "pressure":w_dataset["list"][0]["main"]["pressure"],
                "humidity":w_dataset["list"][0]["main"]["humidity"],
                "sea_level":w_dataset["list"][0]["main"]["sea_level"],


                "weather":w_dataset["list"][1]["weather"][0]["main"],
                "description":w_dataset["list"][1]["weather"][0]["description"],
                "icon":w_dataset["list"][0]["weather"][0]["icon"],
                "icon1":w_dataset["list"][1]["weather"][0]["icon"],
                "icon2":w_dataset["list"][2]["weather"][0]["icon"],
                "icon3":w_dataset["list"][3]["weather"][0]["icon"],
                "icon4":w_dataset["list"][4]["weather"][0]["icon"],
                "icon5":w_dataset["list"][5]["weather"][0]["icon"],
                "icon6":w_dataset["list"][6]["weather"][0]["icon"],

            }
        except:
            context = {

            "city_name":"Not Found, Check your spelling..."
        }
        return render(request, "app_amart/results.html", context)
    else:
    	return redirect('home')


# def social_links(request):
#     sl = Social.objects.all()
#     context = {
#         'sl': sl
#     }
#     return render(request, 'weather_api/base.html', context)