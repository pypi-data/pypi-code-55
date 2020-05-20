from typing import List

import typer
import pytse_client as tse

from stonks_trader.trade_strategies import trade_strategies

app = typer.Typer()


@app.command()
def buy_signals(
        strategies: List[str] = typer.Argument(...),
):
    with typer.progressbar(tse.all_symbols()) as progress:
        result = tse.all_symbols()
        for symbol in progress:
            ticker = tse.Ticker(symbol)
            df = ticker.history
            for strategy in strategies:
                strategy = trade_strategies[strategy](
                    df=df,
                )
                strategy.analyze()
                if not strategy.is_buy_signal():
                    result.remove(symbol)
        for symbol in result:
            print(tse.Ticker(symbol).url)


@app.command()
def update():
    tse.download(symbols="all", write_to_csv=True)

# @app.command()
# def test():
#     df = tse.Ticker("وبملت").history
#     strategy = trade_strategies["macd"](df)
#     strategy.analyze()
#     buy_signal = strategy.df["buy_signal_macd"] == True
#     sell_signal = strategy.df["sell_signal_macd"] == True
#     print(strategy.df[buy_signal | sell_signal])
#     strategy.plot(name=tse.Ticker("وبملت").symbol)
