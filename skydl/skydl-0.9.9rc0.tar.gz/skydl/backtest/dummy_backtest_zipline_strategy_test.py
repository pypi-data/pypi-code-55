from skydl.backtest.simple_zipline_v2.simple_abstract_strategy import SimpleAbstractStrategy
from skydl.common.annotations import Override, print_exec_time


@print_exec_time
class DummyBacktestZiplineStrategy(SimpleAbstractStrategy):

    @Override(SimpleAbstractStrategy)
    def prepare_data(self):
        # zipline数据默认缓存在：~/.zipline/data/
        return None

    @Override(SimpleAbstractStrategy)
    def initialize(self, context):
        # 启动后需要用户干预处理的一次性逻辑
        self.log.info("initialize...")

    @Override(SimpleAbstractStrategy)
    def before_trading_start(self, context, data):
        # 每个bar_open之前执行，对日K可选定当天待交易股票，分钟K在每日盘前可以用于初始化数据
        # self.log.info("before_trading_start...")
        pass

    @Override(SimpleAbstractStrategy)
    def handle_data(self, context, data):
        # 定时执行，处理当前周期中待处理订单
        # self.log.info("handle_data...")
        pass

    @Override(SimpleAbstractStrategy)
    def analyze(self, context, records):
        self.log.info("analyze...")


if __name__ == '__main__':
    DummyBacktestZiplineStrategy().process()
