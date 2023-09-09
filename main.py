from flask import Flask, request, jsonify
import clickhouse_connect
import pandas as pd
import dill
from models import *
import catboost
import lightfm
import pickle
import numpy as np

app = Flask(__name__)
prediction_transformer = False

def get_items_names(items_table):
    client = clickhouse_connect.get_client(host='94.139.255.66', username='danya', password='qwerty')

    items_names = client.query(f"SELECT * FROM {items_table}")

    items_names = pd.DataFrame(data=items_names.result_rows, columns=items_names.column_names)[['item_id', 'name']]
    return items_names

def load_models():

    with open(f"models/popular_model_supermarket_final.pickle", 'rb') as f:
        popular_top_n = pickle.load(f)
        popular_model = popular_top_n
    return popular_model

# def finetune_popular(items, popular_model):
#     for i in items:
#         if i in popular_model.top_items:
#             popular_model.top_items[i] += 1
#     return popular_model
#
# def finetune_model(data):
#     new_data = pd.read_csv(data)
#
#     catboost_model, lightfm_model, cooc_model, popular_model = load_models()
#
#     popular_model = finetune_popular(data['item_id'].values, popular_model)
#     cooc_stats = finetune_cooc(data, cooc_model)
#     cooc_model = CoocurenceRecommender(cooc_stats)
#
#     return
global popular_model
popular_model = load_models()

global item_names
item_names = get_items_names("items_supermarket")

def predict_for_user(user_id, device_id, sequence, recs_number=3):
    return list(popular_model[device_id].keys())[:recs_number]

def get_item_name(item_id):
    name = item_names.loc[item_names['item_id'] == item_id, 'name']
    if len(name) > 0:
        return name.values[0]
    else:
        return "None"


@app.route("/predict_user", methods=['POST'])
def serve_predictions():

    # Parse the user ID from the request
    user_id, device_id, sequence = int(request.json['user_id']), \
        int(request.json['device_id']), \
        list(request.json['items_id'])

    # Get recommendations for the user
    recommendations = predict_for_user(user_id, device_id, sequence, recs_number=3)
    # Return the recommendations as a JSON response

    recommendations = [int(x) for x in recommendations]
    return jsonify(recommendations)

@app.route("/item_name", methods=['POST'])
def get_items():

    # Parse the user ID from the request
    item_ids = list(request.json['item_ids'])

    # Get recommendations for the user
    results = []
    for id in item_ids:
        results.append(get_item_name(id))

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5001)


