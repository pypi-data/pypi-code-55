import matplotlib.pyplot as plt


class AggBackend:
    def __enter__(self):
        self.old_backend = plt.get_backend()
        plt.switch_backend("Agg")

    def __exit__(self, *_, **__):
        plt.switch_backend(self.old_backend)


class FigureCleanMixin:
    def __del__(self):
        if not hasattr(self, "figure"):
            return
        plt.close(self.figure)


class BarPlot(FigureCleanMixin):
    def __init__(self, bars, values, orientation: str = "vertical"):
        with AggBackend():
            self.figure = plt.figure()

            if orientation == "vertical":
                plt.bar(x=bars, height=values)
            elif orientation == "horizontal":
                plt.barh(y=bars, width=values)
            else:
                raise Exception(f"Invalid orientation {orientation}")
