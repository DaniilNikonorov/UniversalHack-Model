from fastapi import Query, APIRouter, UploadFile
from typing import Annotated, Union

from pydantic import BaseModel
from sqlalchemy import or_

from app.database import session
from app.mlmodel.mainmodel import predict_for_user
from app.models import Items, Points, Prediction, UserInfo
from app.mlmodel import mainmodel
import pandas as pd
import logging

router = APIRouter(prefix='/api/v1', tags=['our api'])


@router.get("/offline/market/check/{user_id}")
async def get_market(user_id):
    """Здесь будет получение товаров."""
    try:
        prediction_query = (
            session
            .query(Prediction.item_id)
            .filter(Prediction.user_id == user_id)
        )
        product = prediction_query.first()

        products = (
            session
            .query(UserInfo.item_id)
            .filter(UserInfo.user_id == user_id)
        ).all()

        products.append(product)

        productsWithNames = []
        for p in products:
            productsWithNames.append(
                session
                .query(Items)
                .filter(Items.item_id == int(p))
                .first())

        return {'status': 200, 'result': {
            'user': user_id,
            'predict': product,
            'products': map(lambda n: {'name': n.name, 'item_id': n.item_id}, productsWithNames)
        }}
    except Exception as e:
        print(e)
        logging.error(e)
        return {'status': 500, 'error': str(e)}


@router.post("/offline/market/upload-file")
async def create_market_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        try:
            frame = pd.read_csv(file.file)
            result = []
            for d in frame['device_id']:
                market = await get_market(d)
                result.append(market)

        except Exception as e:
            print(e)
            logging.error(e)
            return {'status': 500, 'error': str(e)}

        """Сюда добавить передачу данных в модель на дообучение"""
        return {'status': 200, 'result': result}


class Item(BaseModel):
    device: int
    items: list


@router.post("/online/market/calculate")
async def calculate(item: Item):
    """Здесь будет получение косметики."""
    try:
        # затычка
        csvdata = {'user_id': 1, 'device_id': item.device, 'items_id': item.items}

        # csvdata = pd.read_csv('filename.csv', sep=';')
        prediction = predict_for_user(user_id=csvdata['user_id'],
                                      device_id=csvdata['device_id'],
                                      sequence=csvdata['items_id']
                                      )
        print('Получилось предскзаать!')
        print(prediction)
        check_query = (
            session
            .query(Items)
            .filter(Items.item_id == prediction)
        )
        result = check_query.first()

        return {'status': 200, 'result': {
            'user': '52644800',
            'product': result.name,
            'products': item.items
        }}
    except Exception as e:
        print(e)
        logging.error(e)
        return {'status': 500, 'error': str(e)}


@router.get("/dictionary/product-by-id/{product_id}")
async def get_product(product_id):
    try:
        check_query = (
            session
            .query(Items)
            .filter(Items.item_id == product_id)
        )

        return {'status': 200, 'result': check_query.all()}
    except Exception as e:
        print(e)
        logging.error(e)
        return {'status': 500, 'error': str(e)}


@router.get("/dictionary/products")
async def get_product():
    try:
        check_query = (
            session
            .query(Items)
            .limit(200)
        )

        return {'status': 200, 'result': check_query.all()}
    except Exception as e:
        print(e)
        logging.error(e)
        return {'status': 500, 'error': str(e)}


@router.get("/dictionary/points")
async def get_points():
    try:
        check_query = (
            session
            .query(Points.receipt_id).distinct()
            .limit(50)
        )

        return {'status': 200, 'result': check_query.all()}
    except Exception as e:
        print(e)
        logging.error(e)
        return {'status': 500, 'error': str(e)}
