from fastapi import Query, APIRouter, UploadFile
from typing import Annotated, Union
from app.database import session
from app.models import Cosmetic, Market
from app.mlmodel import mainmodel
import pandas as pd 

router = APIRouter(prefix='/api/v1/offline', tags=['offline check'])


@router.get("/cosmetic/check/{check_id}")
async def get_cosmetic(check_id):
    """Здесь будет получение косметики."""
    try:
        check_query = (
            session
            .query(Cosmetic)
            .filter(Cosmetic.item_id == check_id) #а где мы фильтры импортируем?
        )
        #затычка
        csvdata = {'user_id': user_id, 'device_id': 352398080550058, 'items_id': [104821, 107726, 100671]}
        response = {"item_ids":[115873, 107726]}

        #csvdata = pd.read_csv('filename.csv', sep=';')
        predictions = predict_for_user(user_id=csvdata['user_id'], 
                                       device_id=csvdata['device_id'], 
                                       sequence=csvdata['items_id']
                                       )

        return {'status': 200, 'result': check_query.all(), 'predictions': predictions}
    except Exception as e:
        return {'status': 500, 'error': str(e)}


@router.get("/market/check/{check_id}")
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


@router.post("/cosmetic/upload-file")
async def create_cosmetic_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        """Сюда добавить передачу данных в модель на дообучение"""
        return {"filename": file.filename}


@router.post("/market/upload-file")
async def create_market_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        """Сюда добавить передачу данных в модель на дообучение"""
        return {"filename": file.filename}
