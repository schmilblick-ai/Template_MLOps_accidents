import sklearn
import pandas as pd 
from sklearn import ensemble
import joblib
import numpy as np
import bentoml
from bentoml.io import NumpyNdarray
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

#print(joblib.__version__)

X_train = pd.read_csv('data/processed/X_train.csv')
X_test = pd.read_csv('data/processed/X_test.csv')
y_train = pd.read_csv('data/processed/y_train.csv')
y_test = pd.read_csv('data/processed/y_test.csv')
y_train = np.ravel(y_train)
y_test = np.ravel(y_test)

rf_classifier = ensemble.RandomForestClassifier(n_jobs = -1)

#--Train the model
rf_classifier.fit(X_train, y_train)

#--Test the model
rf_classifier.predict(X_test)

#--Get the model accuracy
accuracy = rf_classifier.score(X_test, y_test)

print(f"Model accuracy: {accuracy}")

# test the model on a single observation
test_data = X_test.iloc[[0]]

# save test data to a txt file
test_data.to_csv('data/test_data.txt', sep = ',', index = False)
# print the actual label
print(f"Actual label: {y_test[0]}")
# print the predicted label
print(f"Predicted label: {rf_classifier.predict(test_data)[0]}")

# #--Save the trained model to a file
# model_filename = './src/models/trained_model.joblib'
# joblib.dump(rf_classifier, model_filename)
# print("Model trained and saved successfully.")

y_pred=rf_classifier.predict(X_test)

r2_test= r2_score(y_test, y_pred)
#collect the features for bentoml rationalisation and protection
features = list(X_train.columns)

# Enregistrer le modèle dans le Model Store de BentoML
model_ref = bentoml.sklearn.save_model("accidents_rf", rf_classifier, 
    metadata = {
        "r2_test":  round(r2_test, 4),
        "features": features,           # ← ordre ancré ici
    })

print(f"Modèle enregistré sous : {model_ref}")
