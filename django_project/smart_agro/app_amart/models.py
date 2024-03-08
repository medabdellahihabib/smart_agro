from django.db import models

class Message(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.email}"
    
    


# prediction/models.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

crop_dict = {
    'Riz': 1,
    'Maïs': 2,
    'Haricots papillon': 3,
    'Haricot mungo': 4,
    'Haricot noir': 5,
    'Lentille': 6,
    'Banane': 7,
    'Mangue': 8,
    'Raisins': 9,
    'Pastèque': 10,
    'Melon miel': 11,
    'Pomme': 12,
    'Orange': 13,
    'Papaye': 14,
    'Café': 15
}

class CropModel:
    def __init__(self):
        self.rfc = RandomForestClassifier()
        self.ms = MinMaxScaler()

        # Load your CSV data or use your existing DataFrame
        df = pd.read_csv(r'C:\Users\Dell\Desktop\Crop_recommendation_filtered_filtered.csv')

        df['crop_num'] = df['label'].map(crop_dict)

        X = df.drop(['crop_num', 'label'], axis=1)
        y = df['crop_num']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.X_train_scaled = self.ms.fit_transform(X_train)
        self.X_test_scaled = self.ms.transform(X_test)

        self.rfc.fit(self.X_train_scaled, y_train)

    def predict_crop(self, N, P, k, temperature, humidity, ph, rainfall):
        features = np.array([[N, P, k, temperature, humidity, ph, rainfall]])
        transformed_features = self.ms.transform(features)
        prediction = self.rfc.predict(transformed_features)

        return prediction[0]



from django.db import models

class CropProduction(models.Model):
    district = models.CharField(max_length=100)
    crop = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    area = models.FloatField()
    yield1 = models.FloatField()







