from flask import Flask, request, jsonify
import clickhouse_connect
import pandas as pd
import dill
from models import *
import catboost
import lightfm
import pickle

app = Flask(__name__)
prediction_transformer = False

# def classic_model_preds_get(classic_preds_table):
#     client = clickhouse_connect.get_client(host='94.139.255.66', username='danya', password='qwerty')
#
#     interactions_preds = client.query(f"SELECT * FROM {classic_preds_table}")
#
#     interactions_preds = pd.DataFrame(data=interactions_preds.result_rows, columns=interactions_preds.column_names)
#     return interactions_preds

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

def predict_for_user(user_id, device_id, sequence, recs_number=3):
    return list(popular_model['device_id'].keys())[:recs_number]

@app.route("/predict_user", methods=['POST'])
def serve_predictions():

    # Parse the user ID from the request

    user_id, device_id, sequence = int(request.json['user_id']), \
        int(request.json['device_id']), \
        list(request.json['items_id'])

    # Get recommendations for the user
    recommendations = predict_for_user(user_id, device_id, sequence)
    # Return the recommendations as a JSON response
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(port=5001)


