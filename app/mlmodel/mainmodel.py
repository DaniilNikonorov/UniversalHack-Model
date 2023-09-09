#from flask import Flask, request, jsonify
#import clickhouse_connect
import pandas as pd # здесь нужен пандас?
import dill
from app.mlmodel.models import *
import catboost
import lightfm
import pickle

prediction_transformer = False

def load_models():

    print('Try load models!!!!!!!!!!!!!!')
    with open(f"./app/mlmodel/models/popular_model_supermarket_final.pickle", 'rb') as f:
        popular_top_n = pickle.load(f)
        popular_model = popular_top_n # здесь кажется можно одной переменной обойтись

    return popular_model


global popular_model  # надо ли ее глобалом делать ?
popular_model = load_models()

def predict_for_user(user_id, device_id, sequence, recs_number=3):
    return list(popular_model['device_id'].keys())[:recs_number]




