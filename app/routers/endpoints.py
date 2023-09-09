from fastapi import Query, APIRouter, UploadFile
from typing import Annotated, Union
from app.database import session
from app.mlmodel.mainmodel import predict_for_user
from app.models import Cosmetic, Market, Items, Points
from app.mlmodel import mainmodel
import pandas as pd

router = APIRouter(prefix='/api/v1', tags=['our api'])


@router.get("/offline/market/check/{check_id}")
async def get_market(check_id):
    """Здесь будет получение товаров."""
    try:
        check_query = (
            session
            .query(Market)
            .filter(Market.item_id == check_id)
        )

        return {'status': 200, 'result': check_query.all()}
    except Exception as e:
        return {'status': 500, 'error': str(e)}


@router.get("/offline/market/check/{check_id}")
async def get_cosmetic(check_id):
    """Здесь будет получение товаров."""
    try:
        check_query = (
            session
            .query(Market)
            .filter(Market.item_id == check_id)
        )

        return {'status': 200, 'result': check_query.all()}
    except Exception as e:
        return {'status': 500, 'error': str(e)}


@router.post("/offline/cosmetic/upload-file")
async def create_cosmetic_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        frame = pd.read_csv(file.file)

        """Сюда добавить передачу данных в модель на дообучение"""
        return {"filename": frame['check_id']}


@router.post("/offline/market/upload-file")
async def create_market_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        frame = pd.read_csv(file.file)

        """Сюда добавить передачу данных в модель на дообучение"""
        return {"filename": frame['check_id']}


@router.post("/online/market/calculate")
async def get_cosmetic(device, items):
    """Здесь будет получение косметики."""
    try:
        # затычка
        csvdata = {'user_id': 1, 'device_id': device, 'items_id': items}

        # csvdata = pd.read_csv('filename.csv', sep=';')
        prediction = predict_for_user(user_id=csvdata['user_id'],
                                      device_id=csvdata['device_id'],
                                      sequence=csvdata['items_id']
                                      )

        return {'status': 200, 'result': await get_product(prediction)}
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
