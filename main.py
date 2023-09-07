from flask import Flask, request, jsonify
import clickhouse_connect
import pandas as pd
import pickle

app = Flask(__name__)
prediction_transformer = False

def classic_model_preds_get(classic_preds_table):
    client = clickhouse_connect.get_client(host='94.139.255.66', username='danya', password='qwerty')

    interactions_preds = client.query(f"SELECT * FROM {classic_preds_table}")

    interactions_preds = pd.DataFrame(data=interactions_preds.result_rows, columns=interactions_preds.column_names)
    return interactions_preds

# def interactions_data_get(interaction_table):
#     client = clickhouse_connect.get_client(host='94.139.255.66', username='danya', password='qwerty')
#
#     interactions = client.query(f"SELECT * FROM {interaction_table}")
#
#     interactions = pd.DataFrame(data=interactions.result_rows, columns=interactions.column_names)
#     return interactions

global interactions_preds
interactions_preds = classic_model_preds_get("preds_dataset")

# global interactions
# interactions = interactions_data_get("interactions_processed")

global dict_names_items
with open(f"id_title_dict.pkl", 'rb') as f:
    dict_names_items = pickle.load(f)


def predict_for_user(user_id):
    preds = interactions_preds.loc[interactions_preds['user_id'] == user_id]['item_id']
    if len(preds) == 0:
        return [(1, "No user found, here will be popular item")]
    else:
        result_preds = {}
        for value in preds[:5].values:
            value = int(value)
            result_preds[value] = dict_names_items[value]
        return result_preds

# def get_filmes_user(user_id):
#     user_films = interactions_preds.loc[interactions['user_id'] == user_id]['item_id']
#     if len(user_films ) == 0:
#         return [(1, "No films found for user")]
#     else:
#         result_preds = {}
#         for value in user_films.sample(5).values:
#             value = int(value)
#             result_preds[value] = dict_names_items[value]
#         return result_preds

@app.route("/predict_user", methods=['POST'])
def serve_predictions():
    try:
        # Parse the user ID from the request

        user_id = int(request.json['user_id'])

        # Get recommendations for the user
        recommendations = predict_for_user(user_id)
        # Return the recommendations as a JSON response
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)})

# @app.route("/get_user_watched_filmes", methods=['POST'])
# def serve_user_filmes():
#     try:
#         # Parse the user ID from the request
#         user_id = int(request.json['user_id'])
#
#         # Get recommendations for the user
#         recommendations = get_filmes_user(user_id)
#
#         # Return the recommendations as a JSON response
#         return jsonify(recommendations)
#     except Exception as e:
#         return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()

