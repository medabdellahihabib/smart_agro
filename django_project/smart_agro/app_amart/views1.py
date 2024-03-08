from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse



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




from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


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





from django.db import models

file_path = r'C:\Users\Dell\Desktop\smart_agro\django_project\smart_agro\app_amart\Pesticides.csv'


df = pd.read_csv(file_path)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')


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




def predict1(filename, model):
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
    image_files = os.listdir(folder_path)

    random_images = random.sample(image_files, min(num_images, len(image_files)))

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

                class_result, prob_result = predict1(img_path, model)
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
                class_result, prob_result = predict1(img_path, model)
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