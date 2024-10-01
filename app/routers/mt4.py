from datetime import datetime

from fastapi import APIRouter

from app.core.yahoo_fin import YahooFinance
from fastapi.encoders import jsonable_encoder
from app.schemas.mt4_schema import ExampleSchema
from app.models.mt4_model import ExampleModel

router = APIRouter(
    prefix="/ydata",
    tags=["tickers"],
)

@router.get("/")
async def get_data(symbol: str, from_date: str | None = None, to_date: str | None = None):

    data_obj = YahooFinance()
    if from_date and to_date:
        start_date = datetime.strptime(from_date, "%d-%b-%Y")
        end_date = datetime.strptime(to_date, "%d-%b-%Y")
        data = data_obj.fetch_historic_data(symbol, start_date, end_date)
    else:
        data = data_obj.get_live_data(symbol)
    data['symbol'] = symbol
    return jsonable_encoder(data)

@router.get("/live")
async def get_live_stock_price(symbol: str):
    data_obj = YahooFinance()
    return data_obj.get_live_price(symbol)
