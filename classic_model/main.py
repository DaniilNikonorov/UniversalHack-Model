from utils import *
from lightfm import LightFM
from tqdm import tqdm
import dill

train_models = False

interactions, users, items = read_data()
train, test = split_data(interactions)
lfm_train, lfm_pred = lightFMsplit(train)
dataset = createFMDataset(lfm_train)
interactions_matrix, weights_matrix_csr = getInteractionMatrixes(dataset, lfm_train)
lightfm_mapping = userItemMapping(dataset)

if train_models:
    lfm_model = LightFM(
        no_components=64,
        learning_rate=0.1,
        loss='warp',
        max_sampled=5,
        random_state=42
    )

    num_epochs = 20

    for _ in tqdm(range(num_epochs)):
        lfm_model.fit_partial(
            weights_matrix_csr
        )

    with open(f"trained_models/lfm_model.dill", 'wb') as f:
        dill.dump(lfm_model, f)

else:
    with open("trained_models/lfm_model.dill", 'rb') as in_strm:
        lfm_model = dill.load(in_strm)






