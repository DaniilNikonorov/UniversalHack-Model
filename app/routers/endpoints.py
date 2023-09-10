from fastapi import Query, APIRouter, UploadFile
from typing import Annotated, Union
from app.database import session
from app.mlmodel.mainmodel import predict_for_user
from app.models import Items, Points, Prediction, UserInfo
from app.mlmodel import mainmodel
import pandas as pd

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
            .query(Prediction.item_id)
            .filter(UserInfo.user_id == prediction_query.first())
            .limit(10)
        ).all()

        products.append(product)

        productsWithNames = (
            session
            .query(Items)
            .filter(Items.c.item_id.in_([products]))
            .limit(10)
        ).all()

        return {'status': 200, 'result': {
            'user': user_id, 'predict': product, 'products': productsWithNames
        }}
    except Exception as e:
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
            return {'status': 500, 'error': str(e)}

        """Сюда добавить передачу данных в модель на дообучение"""
        return {'status': 200, 'result': result}


@router.post("/online/market/calculate")
async def calculate(device: int, items: list):
    """Здесь будет получение косметики."""
    try:
        # затычка
        csvdata = {'user_id': 1, 'device_id': device, 'items_id': items}

        # csvdata = pd.read_csv('filename.csv', sep=';')
        prediction = predict_for_user(user_id=csvdata['user_id'],
                                      device_id=csvdata['device_id'],
                                      sequence=csvdata['items_id']
                                      )
        check_query = (
            session
            .query(Items)
            .filter(Items.item_id == prediction)
        )

        return {'status': 200, 'result': check_query.first()}
    except Exception as e:
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
        return {'status': 500, 'error': str(e)}
