from typing import List
from collections import Counter
import pandas as pd
from collections import Counter, defaultdict
class PopularRecommender:

    def __init__(
            self,
            top_items: List[int],
    ):
        self.top_items = top_items

    def recommend(self, data):
        data['rank_popular'] = data.apply(lambda row: self._recommend_one_user(row), axis=1)
        return data
    def _recommend_one_user(self, user_data):
        user_item = user_data['item_id']

        if user_item in self.top_items[user_data["device_id"]]:
            count = self.top_items[user_item]
        else:
            count = 300
        return count

class CoocurenceRecommender:

    def __init__(
            self,
            top_pairs,
            item_index: int = 0,
            num_recs: int = 300,
    ):
        self.top_pairs = top_pairs
        self.item_index = item_index
        self.num_recs = num_recs

    def recommend(self, data: [List[int]], inference=False) -> pd.DataFrame:
        recs = [
            self._recommend_one_user(data, inference)
        ]

        return pd.DataFrame({
            'item_id': [item[0] for rec in recs for item in rec],
            f'cooc_score_{self.item_index}': [item[1] for rec in recs for item in rec],
            f'cooc_rank_{self.item_index}': [rnk for rec in recs for rnk, _ in enumerate(rec)],
        })

    def _recommend_one_user(self, user_data: List[int], inference):
        if len(user_data) <= self.item_index:
            return []
        top_pair_items = self.top_pairs.get(user_data[-self.item_index - 1], [])
        us = set(user_data)
        if inference:
            return [item for item in top_pair_items][:self.num_recs]
        return [item for item in top_pair_items if item[0] not in us][:self.num_recs]
