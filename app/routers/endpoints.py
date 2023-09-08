from fastapi import Query, APIRouter, UploadFile
from typing import Annotated, Union
from app.database import session
from app.models import Cosmetic, Market

router = APIRouter(prefix='/api/v1/offline', tags=['offline check'])


@router.get("/cosmetic/check/{check_id}")
async def get_cosmetic(check_id):
    """Здесь будет получение косметики."""
    try:
        check_query = (
            session
            .query(Cosmetic)
            .filter(Cosmetic.item_id == check_id)
        )

        return {'status': 200, 'result': check_query.all()}
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
