from pydantic import BaseModel
from datetime import datetime
from typing import Any, List, Optional



class RouteVariant(BaseModel):
    price: Any
    booking_token: Any


class RouteDate(BaseModel):
    date: datetime
    variant: Optional[RouteVariant]


class Route(BaseModel):
    route: Optional[str]
    dates: List[RouteDate]