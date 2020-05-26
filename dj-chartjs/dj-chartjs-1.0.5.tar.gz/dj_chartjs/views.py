import json
import random
from abc import ABC, abstractmethod

from django.shortcuts import render


class BaseChartView(ABC):

    type_chart = None
    title = None
    legend = False
    beginAtZero = False
    aspectRatio = True
    stepSize = 0.5
    width = 100
    height = 100
    colors = []
    
    def get_tooltips(self):
        return []

    @abstractmethod
    def generate_values(self):
        pass

    def generate_options(self):
        options = {
            "responsive": True,
            "maintainAspectRatio": self.aspectRatio,
            "legend": {"display": self.legend},
            "title": {
                "display": True if self.title is not None else False,
                "text": self.title,
            },
        }
        return options

    @abstractmethod
    def generate_labels(self):
        pass

    def _get_color(self):
        if(len(self.colors) > 0):
            return self.colors
        return "#{:02x}{:02x}{:02x}".format(
            *map(lambda x: random.randint(0, 255), range(3))
        )

    def _get_rgba_from_hex(self, color_hex):
        color = color_hex.lstrip("#")
        rgb = [int(color[i : i + 2], 16) for i in [0, 2, 4]]

        return "rgba({},{},{},0.6)".format(*map(lambda x: x, rgb))

    def get_context_data(self, **kwargs):
        context = {}
        context["chart"] = {
            "data": self.generate_values(),
            "options": self.generate_options(),
            "tooltip": self.get_tooltips() if len(self.get_tooltips()) > 0 else " ",
        }
        context["type"] = self.type_chart
        if self.aspectRatio is not True:
            context["width"] = self.width
            context["height"] = self.height

        return context


class BarChartView(BaseChartView):
    
    type_chart = "bar"

    def _generate_data(self):
        data = {
            "labels": self.generate_labels(),
            "datasets": self._generate_dataset(self.generate_values()),
        }
        return json.dumps(data, ensure_ascii=False)

    def generate_options(self):
        options = super().generate_options()
        options["scales"] = {
            "yAxes": [{"display": True, "ticks": {"beginAtZero": self.beginAtZero,"stepSize": self.stepSize}}]
        }

        return json.dumps(options, ensure_ascii=False)

    def _generate_dataset(self, values):
        collection = []
        dataset = {
            "label": self.get_tooltips() if len(self.get_tooltips()) > 0 else "",
            "backgroundColor": [self._get_color() for entry in self.generate_labels()] if len(self.colors) < 1 else self._get_color(),
            "data": values,
        }
        collection.append(dataset)
        return collection


class RadarChartView(BaseChartView):

    type_chart = "radar"

    def generate_labels(self):
        return []

    def generate_values(self):
        return []

    def create_node(self, label, data, color=None):
        colorData = color if color is not None else self._get_color()
        return {
            "label": label,
            "fill": True,
            "backgroundColor": self._get_rgba_from_hex(colorData),
            "borderColor": colorData,
            "pointBorderColor": "#fff",
            "pointBackgroundColor": colorData,
            "data": list(data),
        }

    def _generate_data(self):
        return json.dumps(
            {"labels": self.generate_labels(), "datasets": self.generate_values()}, ensure_ascii=False
        )

    def generate_options(self):
        options = super().generate_options()
        return json.dumps(options, ensure_ascii=False)


class LineChartView(BaseChartView):

    type_chart = "line"

    """
        the params accept `label` string, and `data` list of values (numeric)
        fill is False to default
    """

    def create_node(self, label, data, fill=False, color=None):
        colorData = color if color is not None else self._get_color()
        return {
            "data": list(data),
            "label": label,
            "borderColor": colorData,
            "backgroundColor": self._get_rgba_from_hex(colorData),
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
        return json.dumps(options, ensure_ascii=False)

    def _get_color(self):
        return "rgba({},{},{},0.4)".format(
            *map(lambda x: random.randint(0, 255), range(5))
        )

    def _generate_data(self):
        return json.dumps(
            {"labels": self.generate_labels(), "datasets": self.generate_values()}, ensure_ascii=False
        )


class GroupChartView(BaseChartView):

    type_bar = "bar"

    def create_node(self, data, label):
        return {
            "label": label,
            "backgroundColor": "#{:02x}{:02x}{:02x}".format(
                *map(lambda x: random.randint(0, 255), range(3))
            ),
            "data": list(data),
        }

    def _generate_data(self):
        return json.dumps(
            {"labels": self.generate_labels(), "datasets": self.generate_values()}, ensure_ascii=False
        )


class HorizontalBarChartView(BarChartView):
    type_chart = "horizontalBar"


class PolarAreaChartView(BarChartView):
    type_chart = "polarArea"


class PieChartView(BarChartView):
    type_chart = "pie"
    position = "top" # top,right, bottom, left

    def generate_options(self):
        options = {
            "legend": {"display": self.legend, "position": self.position},
            "title": {
                "display": True if self.title is not None else False,
                "text": self.title,
            },
        }

        return json.dumps(options, ensure_ascii=False)

    def get_legend_text(self):
        return ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["legend"] = self.get_legend_text()
        return context


class DoughnutChartView(PieChartView):
    type_chart = "doughnut"
