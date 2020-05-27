import json
import random
from abc import ABC, abstractmethod


"""
    Objects represent chartjs instances
"""


class ChartMixin(ABC):

    beginAtZero = True
    aspectRatio = True
    stepSize = 0.5
    title = None
    legend = False
    type_chart = None
    _colors = None
    tooltips = []

    @abstractmethod
    def generate_dataset(self, labels, data):
        """
            `labels` (list) str -> list of string texts
            `data` (list) int or float values -> list values to render in chart
        """
        pass

    def generate_options(self):
        return {
            "responsive": True,
            "maintainAspectRatio": self.aspectRatio,
            "legend": {"display": self.legend},
            "title": {
                "fontSize": 14,
                "display": True if self.title is not None else False,
                "text": self.title if self.title is not None else "",
            },
        }

    def _generate_colors(self, labels):
        return [
            "#{:02x}{:02x}{:02x}".format(
                *map(lambda x: random.randint(0, 255), range(3))
            )
            for entry in labels
        ]

    def set_colors(self, colors):
        self._colors = colors

    def _get_color(self):
        return "#{:02x}{:02x}{:02x}".format(
            *map(lambda x: random.randint(0, 255), range(3))
        )

    def _get_rgba_from_hex(self, color_hex):
        color = color_hex.lstrip("#")
        rgb = [int(color[i : i + 2], 16) for i in [0, 2, 4]]

        return "rgba({},{},{},0.6)".format(*map(lambda x: x, rgb))


class BarChart(ChartMixin):

    type_chart = "bar"

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [
                {
                    "display": True,
                    "ticks": {"beginAtZero": self.beginAtZero, "stepSize": self.stepSize},
                }
            ]
        }
        return options

    def generate_dataset(self, labels, data, dataLabel=""):
        dataset = {
            "labels": list(labels),
            "datasets": [
                {
                    "label": self.tooltips if len(self.tooltips) > 0 else dataLabel,
                    "backgroundColor": self._colors
                    if self._colors is not None
                    else self._generate_colors(labels),
                    "data": list(data),
                }
            ],
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset, ensure_ascii=False),
            "options": json.dumps(self.generate_options(), ensure_ascii=False),
        }


class HorizontalBarChart(ChartMixin):

    type_chart = "horizontalBar"

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "xAxes": [
                {
                    "display": True,
                    "ticks": {"beginAtZero": self.beginAtZero, "stepSize": self.stepSize},
                }
            ]
        }
        return options

    def generate_dataset(self, labels, data, dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [
                {
                    "label": dataLabel if dataLabel is not None else "",
                    "backgroundColor": self._colors
                    if self._colors is not None
                    else self._generate_colors(labels),
                    "data": list(data),
                }
            ],
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset, ensure_ascii=False),
            "options": json.dumps(self.generate_options(), ensure_ascii=False),
        }


class PieChart(ChartMixin):
    type_chart = "pie"
    position = "top" # top,right, bottom, left

    def generate_options(self):
        context = super().generate_options()
        context["legend"] = {"position": self.position}
        return context

    def generate_dataset(self, labels, data, dataLabel=None):
        dataset = {
            "labels": list(labels),
            "datasets": [
                {
                    "label": dataLabel if dataLabel is not None else "",
                    "backgroundColor": self._colors
                    if self._colors is not None
                    else self._generate_colors(labels),
                    "data": list(data),
                }
            ],
        }

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset, ensure_ascii=False),
            "options": json.dumps(self.generate_options(), ensure_ascii=False),
        }


class DoughnutChart(PieChart):
    type_chart = "doughnut"


class PolarAreaChart(PieChart):
    type_chart = "polarArea"


class LineChart(ChartMixin):

    type_chart = "line"

    def create_node(self, label, data, fill=False, color=None):
        """
            this method create special line node, you must pass parameters
            `label` str -> an label individual node, `data`  list -> data render on chart,
            `fill` bool -> default is False, use this to create area chart
            `color` str -> hex color representation (when fill is True)
        """
        colorData = color if color is not None else self._get_color()
        return {
            "data": list(data),
            "label": label,
            "backgroundColor": self._get_rgba_from_hex(colorData),
            "borderColor": colorData,
            "fill": fill,
        }

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [
                {
                    "display": True,
                    "ticks": {"beginAtZero": self.beginAtZero, "stepSize": self.stepSize},
                }
            ]
        }
        return options

    def generate_dataset(self, labels, data):
        dataset = {"labels": labels, "datasets": data}

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset, ensure_ascii=False),
            "options": json.dumps(self.generate_options(), ensure_ascii=False),
        }


class GroupChart(ChartMixin):
    type_chart = "bar"

    def create_node(self, label, data, color=None):
        """
            This method create an special node to group chart:
            `label` -> (str) text to represent individual data
            `data` -> (list) data to render in chart
            `color` -> (str) hex string representation of color, default is None
        """
        colorData = color if color is not None else self._get_color()
        return {"label": label, "backgroundColor": colorData, "data": list(data)}

    def generate_dataset(self, labels, data):
        dataset = {"labels": list(labels), "datasets": list(data)}

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset, ensure_ascii=False),
            "options": json.dumps(self.generate_options(), ensure_ascii=False),
        }


class RadarChart(ChartMixin):

    type_chart = "radar"

    def create_node(self, label, data, color=None):
        colorData = color if color is not None else self._get_rgba_from_hex(color)
        return {
            "label": label,
            "fill": True,
            "backgroundColor": colorData,
            "borderColor": color,
            "pointBorderColor": "#fff",
            "pointBackgroundColor": color,
            "data": list(data),
        }

    def generate_dataset(self, labels, data):
        dataset = {"labels": list(labels), "datasets": list(data)}

        return {
            "type": self.type_chart,
            "data": json.dumps(dataset, ensure_ascii=False),
            "options": json.dumps(self.generate_options(), ensure_ascii=False),
        }
