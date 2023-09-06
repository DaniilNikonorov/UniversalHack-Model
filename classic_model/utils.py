import sys

import lightfm.data
import pandas as pd
from lightfm.data import Dataset
import numpy as np
from sklearn.model_selection import train_test_split

sys.path.append("..")


def read_data():
    interactions = pd.read_csv("../content/interactions_processed.csv")
    users = pd.read_csv("../content/users_processed.csv")
    items = pd.read_csv("../content/items_processed.csv")

    interactions['last_watch_dt'] = pd.to_datetime(interactions['last_watch_dt']).map(lambda x: x.date())

    return interactions, users, items

def split_data(interactions: pd.DataFrame, days=7):
    # Разделяем данные по дням
    max_date = interactions['last_watch_dt'].max()

    train = interactions[(interactions['last_watch_dt'] < max_date - pd.Timedelta(days))]
    test = interactions[(interactions['last_watch_dt'] >= max_date - pd.Timedelta(days))]

    return train, test

def lightFMsplit(train: pd.DataFrame, filter_warm=True):
    # Дополнительно делим по квантилям
    lfm_date_threshold = train['last_watch_dt'].quantile(q=0.6, interpolation='nearest')

    lfm_train = train[(train['last_watch_dt'] < lfm_date_threshold)]
    lfm_pred = train[(train['last_watch_dt'] >= lfm_date_threshold)]

    if filter_warm:
        lfm_pred = lfm_pred[lfm_pred['user_id'].isin(lfm_train['user_id'].unique())]

    return lfm_train, lfm_pred

def createFMDataset(lfm_train: pd.DataFrame) -> lightfm.data.Dataset:
    dataset = Dataset()
    dataset.fit(lfm_train['user_id'].unique(), lfm_train['item_id'].unique())
    return dataset

def getInteractionMatrixes(dataset: lightfm.data.Dataset, lfm_train: pd.DataFrame):
    interactions_matrix, weights_matrix = dataset.build_interactions(
        zip(*lfm_train[['user_id', 'item_id', 'total_dur']].values.T)
    )

    weights_matrix_csr = weights_matrix.tocsr()
    return interactions_matrix, weights_matrix_csr
def userItemMapping(dataset: lightfm.data.Dataset):

    lightfm_mapping = dataset.mapping()
    lightfm_mapping = {
        'users_mapping': lightfm_mapping[0],
        'items_mapping': lightfm_mapping[2],
    }

    lightfm_mapping['users_inv_mapping'] = {v: k for k, v in lightfm_mapping['users_mapping'].items()}
    lightfm_mapping['items_inv_mapping'] = {v: k for k, v in lightfm_mapping['items_mapping'].items()}

    return lightfm_mapping


def generate_lightfm_recs_mapper(model, item_ids, known_items, user_features, item_features, N, user_mapping,
                                 item_inv_mapping, num_threads=4):
    def _recs_mapper(user):
        user_id = user_mapping[user]
        recs = model.predict(user_id, item_ids, user_features=user_features, item_features=item_features,
                             num_threads=num_threads)

        additional_N = len(known_items[user_id]) if user_id in known_items else 0
        total_N = N + additional_N
        top_cols = np.argpartition(recs, -np.arange(total_N))[-total_N:][::-1]

        final_recs = [item_inv_mapping[item] for item in top_cols]
        if additional_N > 0:
            filter_items = known_items[user_id]
            final_recs = [item for item in final_recs if item not in filter_items]
        return final_recs[:N]

    return _recs_mapper

def lightFMmakePreds(lfm_model, lfm_pred, lightfm_mapping):
    top_N = 30

    # вспомогательные данные
    all_cols = list(lightfm_mapping['items_mapping'].values())

    candidates = pd.DataFrame({
        'user_id': lfm_pred['user_id'].unique()
    })

    mapper = generate_lightfm_recs_mapper(
        lfm_model,
        item_ids=all_cols,
        known_items=dict(),
        N=top_N,
        user_features=None,
        item_features=None,
        user_mapping=lightfm_mapping['users_mapping'],
        item_inv_mapping=lightfm_mapping['items_inv_mapping'],
        num_threads=20
    )

    candidates['item_id'] = candidates['user_id'].map(mapper)
    candidates = candidates.explode('item_id')
    candidates['rank'] = candidates.groupby('user_id').cumcount() + 1
    return candidates

def catBoostSplit(lfm_pred: pd.DataFrame):
    ctb_train_users, ctb_test_users = train_test_split(lfm_pred['user_id'].unique(),
                                                       random_state=1,
                                                       test_size=0.2)

    # выделяем 10% под механизм early stopping
    ctb_train_users, ctb_eval_users = train_test_split(ctb_train_users,
                                                       random_state=1,
                                                       test_size=0.1)

    return ctb_train_users, ctb_eval_users, ctb_test_users

def pos_neg_canditates(candidates, lfm_pred: pd.DataFrame):
    pos = candidates.merge(lfm_pred,
                           on=['user_id', 'item_id'],
                           how='inner')

    pos['target'] = 1

    neg = candidates.set_index(['user_id', 'item_id']) \
        .join(lfm_pred.set_index(['user_id', 'item_id']))

    neg = neg[neg['watched_pct'].isnull()].reset_index()
    # добавим сэмплирование, чтобы соблюсти баланс классов
    neg = neg.sample(frac=0.07)
    neg['target'] = 0

    return neg, pos

