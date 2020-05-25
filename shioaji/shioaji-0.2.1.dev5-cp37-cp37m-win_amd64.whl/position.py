from shioaji.base import BaseModel
from shioaji.contracts import Contract
from shioaji.constant import Action, StockOrderCond
from shioaji.account import Account
import typing


class Position(BaseModel):
    code: str
    direction: Action
    quantity: int
    price: float
    pnl: float
    yd_quantity: int
    cond: StockOrderCond = StockOrderCond.Cash


class Positions(BaseModel):
    positions: typing.List[Position]
    account: Account


class ProfitLoss(BaseModel):
    code: str
    seqno: str
    quantity: int
    price: float
    pnl: float
    pr_ratio: float
    cond: StockOrderCond = StockOrderCond.Cash
    date: str


class ProfitLossList(BaseModel):
    profitloss: typing.List[ProfitLoss]
    account: Account
