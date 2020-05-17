from coverage_strategies import CircleOutsideFromCornerAdjacentToIo_Strategy
from coverage_strategies.CircleInsideFromCornerFarthestFromIo_Strategy import \
    CircleInsideFromCornerFarthestFromIo_Strategy
from coverage_strategies.CircleOutsideFromBoardCenter_Strategy import CircleOutsideFromBoardCenter_Strategy
from coverage_strategies.CircleOutsideFromCornerFarthestFromIo_Strategy import \
    CircleOutsideFromCornerFarthestFromIo_Strategy
from coverage_strategies.CircleOutsideFromIo_Strategy import CircleOutsideFromIo_Strategy
from coverage_strategies.CoverByQuarters_Strategy import CoverByQuarters_Strategy
from coverage_strategies.Entities import StrategyEnum
from coverage_strategies.HorizontalCircularCoverage_Strategy import HorizontalCircularCoverage_Strategy
from coverage_strategies.InterceptThenCopy_Strategy import InterceptThenCopy_Strategy
from coverage_strategies.LCP_Strategy import LCP_Strategy
from coverage_strategies.LongestToReach_Strategy import LongestToReach_Strategy
from coverage_strategies.STC_Strategy import STC_Strategy
from coverage_strategies.TrulyRandom_Strategy import TrulyRandomStrategy
from coverage_strategies.VerticalCircularCoverage_Strategy import VerticalCircularCoverage_Strategy
from coverage_strategies.VerticalCoverageFromCornerFarthestFromIo_Strategy import \
    VerticalCoverageFromCornerFarthestFromIo_Strategy
from coverage_strategies.VerticalNonCircularCoverage_Strategy import VerticalNonCircularCoverage_Strategy


def get_strategy_from_enum(strategy_enum: StrategyEnum):
    if strategy_enum == StrategyEnum.VerticalCoverageCircular:
        return VerticalCircularCoverage_Strategy()
    elif strategy_enum == StrategyEnum.HorizontalCoverageCircular:
        return HorizontalCircularCoverage_Strategy()
    elif strategy_enum == StrategyEnum.FullKnowledgeInterceptionCircular:
        return InterceptThenCopy_Strategy()
    elif strategy_enum == StrategyEnum.QuartersCoverageCircular:
        return CoverByQuarters_Strategy()
    elif strategy_enum == StrategyEnum.RandomSTC:
        return STC_Strategy()
    elif strategy_enum == StrategyEnum.VerticalCoverageNonCircular:
        return VerticalNonCircularCoverage_Strategy()
    elif strategy_enum == StrategyEnum.SpiralingIn:
        return CircleInsideFromCornerFarthestFromIo_Strategy()
    elif strategy_enum == StrategyEnum.SpiralingOut:
        return CircleOutsideFromBoardCenter_Strategy()
    elif strategy_enum == StrategyEnum.VerticalFromFarthestCorner_OpponentAware:
        return VerticalCoverageFromCornerFarthestFromIo_Strategy()
    elif strategy_enum == StrategyEnum.SemiCyclingFromFarthestCorner_OpponentAware:
        return CircleOutsideFromCornerFarthestFromIo_Strategy()
    elif strategy_enum == StrategyEnum.SemiCyclingFromAdjacentCorner_col_OpponentAware:
        return CircleOutsideFromCornerAdjacentToIo_Strategy.CircleOutsideFromCornerAdjacentToIo_Strategy(False)
    elif strategy_enum == StrategyEnum.SemiCyclingFromAdjacentCorner_row_OpponentAware:
        return CircleOutsideFromCornerAdjacentToIo_Strategy.CircleOutsideFromCornerAdjacentToIo_Strategy(True)
    elif strategy_enum == StrategyEnum.CircleOutsideFromIo:
        return CircleOutsideFromIo_Strategy()
    elif strategy_enum == StrategyEnum.LCP:
        return LCP_Strategy()
    elif strategy_enum == StrategyEnum.LONGEST_TO_REACH:
        return LongestToReach_Strategy()
    elif strategy_enum == StrategyEnum.TRULY_RANDOM:
        return TrulyRandomStrategy()