from pydantic import BaseModel,Field
from datetime import datetime

class Strategy_Input(BaseModel):
    strat_name: str
    symbol : str=Field(...,description="strat not required for now")
    start_date:datetime=Field(..., description="The start date for the backtest")
    end_date:datetime=Field(..., description="The start date for the backtest")
    short_window:int = Field(..., gt=0, description="Short-term moving average period (must be > 0)")
    long_window: int =Field(..., gt=0, description="Short-term moving average period (must be > 0)")

class Rsi_Input(BaseModel):
    strat_name: str
    symbol : str=Field(...,description="strat not required for now")
    start_date:datetime=Field(..., description="The start date for the backtest")
    end_date:datetime=Field(..., description="The start date for the backtest")
