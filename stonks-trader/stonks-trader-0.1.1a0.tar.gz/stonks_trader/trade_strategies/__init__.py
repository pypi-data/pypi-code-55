from typing import Dict, Type

from .bollinger import BollingerBandsStrategy
from .compression import CompressionStrategy
from .macd import MACDStrategy
from .rsi import RsiStrategy
from .sma import SmaStrategy
from .stochastic import StochasticStrategy
from .strategy import TradingStrategy

trade_strategies: Dict[str, Type[TradingStrategy]] = {
    "rsi": RsiStrategy,
    "stochastic": StochasticStrategy,
    "macd": MACDStrategy,
    "bollinger-bands-trend": BollingerBandsStrategy,
    "sma-cross": SmaStrategy,
    "compression": CompressionStrategy,
}
