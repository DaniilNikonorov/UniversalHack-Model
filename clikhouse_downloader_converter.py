import clickhouse_connect
from pathlib import Path

def data_tranform_to_recbole(interactions_name, users_name,
                             items_names, save_dataset_name):
    """
    Class to download data from out clickhouse and trnaform it into recbole format
    https://recbole.io/docs/user_guide/usage/running_new_dataset.html#
    :return: nothing, just create files in folders
    """
    client = clickhouse_connect.get_client(host='94.139.255.66', username='danya', password='qwerty')

    directory = Path(save_dataset_name)
    directory.mkdir(parents=True, exist_ok=True)

    interactions = client.query(f"SELECT * FROM {interactions_name}")

    interactions_df = pd.DataFrame(data = interactions.result_rows, columns = interactions.column_names)
    interactions_df['last_watch_dt'] = pd.to_datetime(interactions_df['last_watch_dt'], format='%Y-%m-%d')
    interactions_df['timestamp'] = interactions_df.last_watch_dt.values.astype(np.int64) // 10 ** 9
    interactions_df.drop(['total_dur', 'last_watch_dt'], axis=1, inplace=True)
    interactions_df = interactions_df.rename(columns={'watched_pct': 'rating'})

    interactions_df.to_csv(f'{save_dataset_name}/{save_dataset_name}.inter', sep='\t',
                           index=False, header=['user_id:token', 'item_id:token',
                                                'rating:float', 'timestamp:float'], float_format='%d')

    client = clickhouse_connect.get_client(host='94.139.255.66', username='danya', password='qwerty')

    users = client.query(f"SELECT * FROM {users_name}")
    users_df = pd.DataFrame(data = users.result_rows, columns = users.column_names)
    users_df.to_csv(f'{save_dataset_name}/{save_dataset_name}.user', sep='\t', index=False, header=['user_id:token', 'age:token', 'income:token',
                                    'sex:token', 'kids_flg:token'], float_format='%d')

    client = clickhouse_connect.get_client(host='94.139.255.66', username='danya', password='qwerty')

    items = client.query(f"SELECT * FROM {items_names}")
    items_df = pd.DataFrame(data = items.result_rows, columns = items.column_names)
    items_df.to_csv(f'{save_dataset_name}/{save_dataset_name}.item', sep='\t', index=False, header=['item_id:token', 'content_type:token', \
                                     'title:token_seq', 'title_orig:token_seq', \
                                     'genres:token_seq', 'countries:token', 'for_kids:token', 'age_rating:float', 'studios:token', \
                                     'directors:token', \
                                     'actors:token_seq', 'description:token_seq', 'keywords:token_seq', \
                                     'release_year_cat:token'], float_format='%d')

if __name__ == "__main__":
    data_tranform_to_recbole("interactions_processed_2", "kion_users", "kion_items", "content/kion")