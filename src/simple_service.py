# src/simple_service.py
import numpy as np
import pandas as pd
import bentoml
from bentoml.models import BentoModel
from pydantic import BaseModel, Field, ConfigDict

class InputModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    place: int
    catu: int
    sexe: int
    secu1: float
    year_acc: int
    victim_age: int
    catv: int
    obsm: int
    motor: int
    catr: int
    circ: int
    surf: int
    situ: int
    vma: int
    jour: int
    mois: int
    lum: int
    dep: int
    com: int
    agg_: int
    int_: int #= Field(alias="int")
    atm: int
    col: int
    lat: float
    long: float
    hour: int
    nb_victim: int
    nb_vehicules: int

@bentoml.service()
class RFClassifierService:
    #model_ref = bentoml.models.get("accidents_rf:latest")
    model_ref = BentoModel("accidents_rf:latest")
    def __init__(self):
        self.model = bentoml.sklearn.load_model(self.model_ref)
        # To be tested, it can be a non existing practice
        try:
            self.features = self.model_ref.info.metadata["features"]
        except BaseException as e:
            raise (f"Please save the feature list in the metadata model {e}") 


    @bentoml.api(route="/predict")
    def predict(self, input_data: InputModel) -> dict:

        #--- checking alignment of pydantic and model def
        #this only valid if input_data is considered a dict in def predict statement, not a pydantic
        #missing = set(self.features) - set(input_data.keys())
        #we retrieve the model_fields from the sub declared InputModel

        pydantic_input_fields = {
            info.alias or name
            for name, info in InputModel.model_fields.items()
        }
        model_features=set(self.features)
        print(model_features,pydantic_input_fields,sep="\n\n")
        missing_in_pydantic = model_features - pydantic_input_fields  # features du modèle absentes du schema
        extra_in_pydantic   = pydantic_input_fields - model_features    # champs Pydantic inconnus du modèle

        if missing_in_pydantic:
            raise RuntimeError(
                f"AdmissionInput manque ces features du modèle : {missing_in_pydantic}"
            )
        if extra_in_pydantic:
            raise RuntimeError(
                f"AdmissionInput a des champs inconnus du modèle : {extra_in_pydantic}"
            )
        # -- Si on arrive ici, schema Pydantic et modèle sont en phase --------
        print("✅ Schema Pydantic aligné avec les features du modèle")

        
        # Reconstruction dans l'ordre des features du training — peu importe l'ordre du dict entrant
        #Dict approach - sample = pd.DataFrame([[input_data[f] for f in self.features]],columns=self.features)
        
        #pydantic approach - alignement du sample à prédir
        sample = pd.DataFrame([[getattr(input_data, f.replace(" ", "_")) for f in self.features]], columns=self.features )

        pred = self.model.predict(sample)
        return {"prediction": pred.tolist()}
