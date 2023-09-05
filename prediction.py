from recbole.utils.case_study import full_sort_topk
import pickle
from flask import Flask, request, jsonify
import torch
from recbole.utils import init_logger, get_model, init_seed
from recbole.data import create_dataset, data_preparation
from logging import getLogger

app = Flask(__name__)

def load_data_and_model(model_file):
    r"""Load filtered dataset, split dataloaders and saved model.

    Args:
        model_file (str): The path of saved model file.

    Returns:
        tuple:
            - config (Config): An instance object of Config, which record parameter information in :attr:`model_file`.
            - model (AbstractRecommender): The model load from :attr:`model_file`.
            - dataset (Dataset): The filtered dataset.
            - train_data (AbstractDataLoader): The dataloader for training.
            - valid_data (AbstractDataLoader): The dataloader for validation.
            - test_data (AbstractDataLoader): The dataloader for testing.
    """

    checkpoint = torch.load(model_file, map_location=torch.device('cpu'))
    config = checkpoint["config"]

    init_seed(config["seed"], config["reproducibility"])
    init_logger(config)
    logger = getLogger()
    logger.info(config)
    config['data_path'] = "/Users/vladimiragishev/Desktop/Code/Python/RecSys/UniversalRecSys-Hack/content/kion"

    dataset = create_dataset(config)
    logger.info(dataset)
    train_data, valid_data, test_data = data_preparation(config, dataset)

    init_seed(config["seed"], config["reproducibility"])
    model = get_model(config["model"])(config, train_data._dataset).to("cpu")
    model.load_state_dict(checkpoint["state_dict"])
    model.load_other_parameter(checkpoint.get("other_parameter"))

    return config, model, dataset, train_data, valid_data, test_data

def predict_for_user(user_id):
    if torch.cuda.is_available():
        map_location = torch.device('cuda')
    else:
        map_location = torch.device('cpu')

    with open("data/id_title_dict.pkl", 'rb') as pickle_file:
        loaded_dict = pickle.load(pickle_file)
    uid_series = dataset.token2id(dataset.uid_field, ['19'])
    # uid_series[0] = user_id
    topk_score, topk_iid_list = full_sort_topk(uid_series, model, test_data, k=10, device="cpu")
    external_item_list = dataset.id2token(dataset.iid_field, topk_iid_list.cpu())
    return [loaded_dict.get(int(id), 'Unknown') for id in list(external_item_list[0])]


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

config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
    model_file='models/SASRec-v0.1.pth'
)

if __name__ == "__main__":
    app.run()
