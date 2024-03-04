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
            image_path = f"images/{result_label}.jpeg"  

            return render(request, 'app_amart/nn.html', {'result': (result_label, result_crop), 'image_path': image_path, 'form': form})
    else:
        form = CropPredictionForm()

    return render(request, 'app_amart/nn.html', {'form': form})




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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard1(request):
    return render(request, "app_amart/dashboard.html", {'section': 'dashboard1', 'user': request.user})
""" 
from django.shortcuts import render
import pickle
import numpy as np
from .forms import CropProductionForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def predict_prod(request):
    if request.method == 'POST':
        form = CropProductionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            model = pickle.load(open("model.pkl", "rb"))
            result = model.predict(np.array([data['district'], data['crop'], data['season'], data['area'], data['yield1']]).reshape(1, -1))
            result = float(result[0])
            return render(request, 'app_amart/forecast.html', {'result': result})
        else:
            print(form.errors)
    else:
        form = CropProductionForm()
    return render(request, 'app_amart/index.html', {'form': form})   """


# views.py

from django.shortcuts import render
import pickle
import numpy as np

# Charger le modèle
model = pickle.load(open("model.pkl", "rb"))
label_encoding_info = {
    "District": {
        "Jodhpur": 5,
        "Kota": 6,
        "Jaipur": 4,
        "Hanumangarh": 3,
        "Sri Ganganagar": 8,
        "Udaipur": 9,
        "Bhilwara": 2,
        "Alwar": 1,
        "Nagaur": 7,
        "Ajmer": 0,
    },
    "Crop": {
        "Wheat": 22,
        "Gram": 10,
        "Coriander": 4,
        "Citrus": 3,
        "Cotton": 5,
        "Guava": 11,
        "Garlic": 9,
        "Mustard": 14,
        "Fenugreek": 8,
        "Maize": 12,
        "Fennel": 7,
        "Bajra": 0,
        "Oilseeds": 15,
        "Opium": 17,
        "Pomegranate": 18,
        "Cumin": 6,
        "Chilli": 2,
        "Tomato": 21,
        "Sugarcane": 20,
        "Barley": 1,
        "Onion": 16,
        "Pulses": 19,
        "Mango": 13,
    },
    "Season": {"Kharif": 0, "Rabi": 1},
}

def inde(request):
    return render(request, "app_amart/index.html")

def predict_prod(request):
    if request.method == "POST":
        user_input = ["District", "Crop", "Season", "Area", "Yield"]
        decoded_input = {}

        for i in user_input[:3]:
            encoding_map = label_encoding_info[i]
            decoded_value = encoding_map[request.POST.get(i)]
            decoded_input[i] = decoded_value

        data = [decoded_input[i] for i in user_input[:3]]
        data.extend(float(request.POST.get(i)) for i in user_input[3:])

        district, crop, season = (
            request.POST.get("District"),
            request.POST.get("Crop"),
            request.POST.get("Season"),
        )
        area, yield1 = float(request.POST.get("Area")), float(request.POST.get("Yield"))

        result = model.predict(np.array(data).reshape(1, -1))

        result = float(result[0])
        return render(
            request,
            "app_amart/forecast.html",
            {
                "district": district,
                "crop": crop,
                "season": season,
                "area": area,
                "yield1": yield1,
                "result": result,
            },
        )
        

def test_again(request):
    return render(request, "app_amart/index.html")


from django.shortcuts import render

def contact_vie(request):
    return render(request, 'contact1.html')






# adventure 


from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import os
import uuid
import urllib
import cv2
import base64
import pandas as pd
import numpy as np
import tensorflow 
from PIL import Image
from keras_preprocessing.image import load_img, img_to_array
from keras.models import load_model
from keras.applications.mobilenet import MobileNet, preprocess_input




from tensorflow.keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense ,Flatten ,Conv2D ,MaxPooling2D ,Dropout ,BatchNormalization
from keras.optimizers import Adam 
from keras.callbacks import EarlyStopping ,ReduceLROnPlateau , ModelCheckpoint
from keras.applications.mobilenet import MobileNet ,preprocess_input
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)
optimizer=Adam(lr=0.001,beta_1=0.9,beta_2=0.99)
# from flask import Flask , render_template  , request , send_file, Response
from keras_preprocessing.image import load_img , img_to_array
import cv2
import base64
import pandas as pd
import numpy as np
import sys
sys.path.append("./lib")


import pathlib
import random


from .lib import Dataloader
from .lib import modeler



# Django imports
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Autres imports Django
import os
import uuid
import urllib
from PIL import Image
import cv2
import base64
import pandas as pd
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model





# Modèles Django
from django.db import models

file_path = r'C:\Users\Dell\Desktop\smart_agro\django_project\smart_agro\app_amart\Pesticides.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Définition des modèles
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')

# Chargement du modèle Keras
def load_keras_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return load_model(os.path.join(base_dir, 'mobilenet_final.hdf5'))

model = load_keras_model()

classes = ['Adristyrannus','Aleurocanthus spiniferus','alfalfa plant bug','alfalfa seed chalcid','alfalfa weevil','Ampelophaga','aphids',
           'Aphis citricola Vander Goot','Apolygus lucorum','army worm','asiatic rice borer','Bactrocera tsuneonis','beet army worm','beet fly',
           'Beet spot flies','beet weevil','beetle','bird cherry-oataphid','black cutworm','Black hairy','blister beetle','bollworm',
           'Brevipoalpus lewisi McGregor','brown plant hopper','cabbage army worm','cerodonta denticornis','Ceroplastes rubens','Chlumetia transversa',
           'Chrysomphalus aonidum','Cicadella viridis','Cicadellidae','Colomerus vitis','corn borer','corn earworm','cutworm','Dacus dorsalis(Hendel)',
           'Dasineura sp','Deporaus marginatus Pascoe','english grain aphid','Erythroneura apicalis','fall armyworm','Field Cricket','flax budworm',
           'flea beetle','Fruit piercing moth','Gall fly','grain spreader thrips','grasshopper','green bug','grub','Icerya purchasi Maskell','Indigo caterpillar',
           'Jute aphid','Jute hairy','Jute red mite','Jute semilooper','Jute stem girdler','Jute Stem Weevil','Jute stick insect','large cutworm',
           'Lawana imitata Melichar','Leaf beetle','legume blister beetle','Limacodidae','Locust','Locustoidea','longlegged spider mite','Lycorma delicatula',
           'lytta polita','Mango flat beak leafhopper','meadow moth','Mealybug','Miridae','mites','mole cricket','Nipaecoccus vastalor','odontothrips loti',
           'oides decempunctata','paddy stem maggot','Panonchus citri McGregor','Papilio xuthus','parathrene regalis','Parlatoria zizyphus Lucus','peach borer',
           'penthaleus major','Phyllocnistis citrella Stainton','Phyllocoptes oleiverus ashmead','Pieris canidia','Pod borer','Polyphagotars onemus latus',
           'Potosiabre vitarsis','Prodenia litura','Pseudococcus comstocki Kuwana','red spider','Rhytidodera bowrinii white','rice gall midge','rice leaf caterpillar',
           'rice leaf roller','rice leafhopper','rice shell pest','Rice Stemfly','rice water weevil','Salurnis marginella Guerr','sawfly','Scirtothrips dorsalis Hood',
           'sericaorient alismots chulsky','small brown plant hopper','Spilosoma Obliqua','stem borer','Sternochetus frigidus','tarnished plant bug','Termite',
           'Termite odontotermes (Rambur)','Tetradacus c Bactrocera minax','therioaphis maculata Buckton','Thrips','Toxoptera aurantii','Toxoptera citricidus',
           'Trialeurodes vaporariorum','Unaspis yanonensis','Viteus vitifoliae','wheat blossom midge','wheat phloeothrips','wheat sawfly','white backed plant hopper',
           'white margined moth','whitefly','wireworm','Xylotrechus','yellow cutworm','Yellow Mite','yellow rice borer']



# Fonction pour prédire
def predict(filename, model):
    img = load_img(filename, target_size=(224, 224))
    img = img_to_array(img)
    img = img.reshape(1, 224, 224, 3)
    img = img.astype('float32')
    img = img / 255.0
    result = model.predict(img)
    dict_result = {result[0][i]: classes[i] for i in range(132)}
    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]
    prob_result = []
    class_result = []
    for i in range(3):
        prob_result.append((prob[i] * 100).round(2))
        class_result.append(dict_result[prob[i]])
    return class_result, prob_result
def get_random_images(folder_path, num_images=3):
    # Liste des noms de fichiers des images dans le dossier
    image_files = os.listdir(folder_path)

    # Sélectionnez 'num_images' images au hasard
    random_images = random.sample(image_files, min(num_images, len(image_files)))

    # Retourne les chemins complets des images sélectionnées
    return [os.path.join(folder_path, img) for img in random_images]

def success(request):
    error = ''
    if request.method == 'POST':
        if request.POST.get('link'):
            link = request.POST.get('link')
            try:
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename + ".jpg"
                img_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
                output = open(img_path, "wb")
                output.write(resource.read())
                output.close()
                img = filename

                class_result, prob_result = predict(img_path, model)
                predictions = {
                    "class1": class_result[0],
                    "class2": class_result[1],
                    "class3": class_result[2],
                    "prob1": prob_result[0],
                    "prob2": prob_result[1],
                    "prob3": prob_result[2],
                }

            except Exception as e:
                print(str(e))
                error = 'Cette image n\'est pas accessible ou n\'est pas un format valide'
        elif request.FILES.get('file'):
            file = request.FILES['file']
            if file.name.split('.')[-1] in ['jpg', 'jpeg', 'png']:
                filename = default_storage.save(os.path.join('uploads', file.name), ContentFile(file.read()))
                img_path = os.path.join(settings.MEDIA_ROOT, filename)
                class_result, prob_result = predict(img_path, model)
                predictions = {
                    "class1": class_result[0],
                    "class2": class_result[1],
                    "class3": class_result[2],
                    "prob1": prob_result[0],
                    "prob2": prob_result[1],
                    "prob3": prob_result[2],
                }
                class_result_lower = [class_name.lower() for class_name in class_result]
        # Find the index of the row where the class matches
                row_index = (df.iloc[:, 0].str.lower() == class_result_lower[0]).idxmax()
                
                folder_path = 'C:/Users/Dell/Desktop/smart_agro/django_project/smart_agro/app_amart/static/test1/'

    # Obtenez trois images au hasard
                random_images = get_random_images(folder_path)

    # Imprime les noms de fichiers sans leurs extensions
                l = [os.path.splitext(os.path.basename(img))[0] for img in random_images]

        
                pesticide_text = f"Common pesticides used for controlling {df.iloc[row_index, 0]} are {df.iloc[row_index, 1]}"
                return render(request, 'success.html', {'img': filename, 'images': l,'predictions': predictions, 'pesticide_text': pesticide_text})
        
            else:
                error = "Veuillez télécharger uniquement des images aux formats jpg, jpeg ou png"
    return render(request, 'index.html', {'error': error})



# Vue pour la webcam
def cam(request):
    return render(request, 'cam.html')


import cv2
from django.http import StreamingHttpResponse

def gen_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    # Initialisez votre caméra ici, par exemple :
    camera = cv2.VideoCapture(0)
    
    return StreamingHttpResponse(gen_frames(camera), content_type='multipart/x-mixed-replace; boundary=frame')



import cv2

def capture(camera):
    success, frame = camera.read()
    if success:
        cv2.imwrite('captured_image.jpg', frame)
        return 'Image captured successfully!'
    else:
        return 'Failed to capture image.'

# Vue pour sauvegarder une image
import base64
from django.http import HttpResponse

import base64
from django.http import HttpResponse

def save(request):
    if 'imageData' in request.POST:
        
        data_url = request.POST['imageData']
        img_data = base64.b64decode(data_url.split(',')[1])
        with open('capture.jpg', 'wb') as f:
            f.write(img_data)
        return HttpResponse('Image saved as capture.jpg')
    else:
        return HttpResponse('No image data found in the request.')

# Assurez-vous d'avoir configuré les paramètres pour les fichiers téléchargés dans votre fichier settings.py
# Par exemple, pour spécifier le dossier de téléchargement et les types de fichiers autorisés, vous pouvez le faire comme suit :

# settings.py

# Définissez le dossier de téléchargement et les types de fichiers autorisés
UPLOAD_FOLDER = './DATASET'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Vous pouvez également définir le répertoire de téléchargement dans les paramètres de votre vue, si nécessaire


# Vue pour la rétroaction
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect

def upload_file(request):
    if request.method == 'POST':
        # get the checkbox value and create a directory with that name
        checkbox_value = request.POST.get('checkbox')
        upload_folder = './DATASET'  # or specify your desired upload folder
        
        if not os.path.exists(os.path.join(upload_folder, checkbox_value)):
            os.makedirs(os.path.join(upload_folder, checkbox_value))

        # get the uploaded file and save it to the directory
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name
        file_path = os.path.join(upload_folder, checkbox_value, filename)
        with open(file_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Optionally, you can perform additional tasks here, such as retraining the model
        
        # Redirect to another page after successful file upload
        return HttpResponseRedirect('/loader/')  # Change '/loader/' to your desired URL
        
    # render the HTML template with the checkboxes
    return render(request, 'upload.html')


DATASET = './DATASET'  

    
def stoptrainer(request):
    return render_template('index.html')

def hom(request):
    return render(request, "index.html")

import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.layers import MaxPooling2D, Flatten, Dense, BatchNormalization
from tensorflow.keras.models import Sequential

DATASET = './DATASET'

def retrainer(request, path=DATASET):
    if request.method == 'POST':
        training, testing, validing = Dataloader.dataloader(path)
        
        # Charger le modèle pré-entraîné MobileNet
        mobilenet = MobileNet(include_top=False, weights='imagenet', input_shape=(224,224,3))
        mobilenet.trainable = False
        
        # Ajouter des couches au modèle MobileNet pour l'adapter à vos données
        mob_model = Sequential([
            mobilenet,
            MaxPooling2D(3, 2),
            Flatten(),
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dense(1024, activation='relu'),
            BatchNormalization(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dense(132, activation='softmax')
        ])
        
        # Compiler le modèle
        optimizer = 'adam'  # Définissez votre optimiseur ici
        mob_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=["accuracy", "Precision", "Recall", "AUC"])
        
        # Entraîner le modèle
        epochs = 10
        batch_size = 32
        steps_per_epoch = training.n // batch_size
        validation_steps = validing.n // batch_size
        
        print("[INFO] Starting Model Training")
        history_mob = mob_model.fit(training, validation_data=validing, epochs=epochs, batch_size=batch_size,
                                    steps_per_epoch=steps_per_epoch, validation_steps=validation_steps, verbose=1)
        print("[INFO] Model Training Complete")
        
        # Sauvegarder le modèle
        print("[INFO] Saving Model")
        try:
            os.remove("mobilenet_retrained.hdf5")
            mob_model.save('mobilenet_retrained.hdf5')
        except FileNotFoundError:
            pass
        except Exception as e:
            return HttpResponse(f"Error while saving model: {str(e)}", status=500)
        
        print("[INFO] Retrained Model Saved")
        
        return HttpResponse("Model Training complete, Please return to homepage")
    
    return render(request, 'retrain.html')  # Assurez-vous d'avoir un template retrain.html dans votre répertoire de templates

  
  
from django.shortcuts import render
import os
import random


import os
import random
from django.shortcuts import render

def get_random_images(folder_path, num_images=3):
    # Liste des noms de fichiers des images dans le dossier
    image_files = os.listdir(folder_path)

    # Sélectionnez 'num_images' images au hasard
    random_images = random.sample(image_files, min(num_images, len(image_files)))

    # Retourne les chemins complets des images sélectionnées
    return [os.path.join(folder_path, img) for img in random_images]

def ma(request):
    # Chemin vers le dossier contenant les images
    folder_path = 'C:/Users/Dell/Desktop/smart_agro/django_project/smart_agro/app_amart/static/test1/'

    # Obtenez trois images au hasard
    random_images = get_random_images(folder_path)

    # Imprime les noms de fichiers sans leurs extensions
    l = [os.path.splitext(os.path.basename(img))[0] for img in random_images]

    return render(request, 'votre_template.html', {'images': l})
