import os

from jinja2 import Environment, FileSystemLoader

from pyecharts.commons.utils import JsCode


class _RenderType:
    CANVAS = "canvas"
    SVG = "svg"


class _FileType:
    SVG = "svg"
    PNG = "png"
    JPEG = "jpeg"
    HTML = "html"


class _SymbolType:
    RECT = "rect"
    ROUND_RECT = "roundRect"
    TRIANGLE = "triangle"
    DIAMOND = "diamond"
    ARROW = "arrow"


class _ChartType:
    BAR = "bar"
    BAR3D = "bar3D"
    BOXPLOT = "boxplot"
    EFFECT_SCATTER = "effectScatter"
    FUNNEL = "funnel"
    GAUGE = "gauge"
    GEO = "geo"
    GRAPH = "graph"
    HEATMAP = "heatmap"
    KLINE = "candlestick"
    LINE = "line"
    LINE3D = "line3D"
    LINES = "lines"
    LINES3D = "lines3D"
    LIQUID = "liquidFill"
    MAP = "map"
    MAP3D = "map3D"
    PARALLEL = "parallel"
    PICTORIALBAR = "pictorialBar"
    PIE = "pie"
    POLAR = "polar"
    RADAR = "radar"
    SANKEY = "sankey"
    SCATTER = "scatter"
    SCATTER3D = "scatter3D"
    SUNBURST = "sunburst"
    THEMERIVER = "themeRiver"
    TREE = "tree"
    TREEMAP = "treemap"
    WORDCLOUD = "wordCloud"
    CUSTOM = "custom"


ToolTipFormatterType = {
    _ChartType.GEO: JsCode(
        """function (params) {
        return params.name + ' : ' + params.value[2];
    }"""
    ),
    _ChartType.GAUGE: "{a} <br/>{b} : {c}%",
}


class _ThemeType:
    BUILTIN_THEMES = ["light", "dark", "white"]
    LIGHT = "light"
    DARK = "dark"
    WHITE = "white"
    CHALK = "chalk"
    ESSOS = "essos"
    INFOGRAPHIC = "infographic"
    MACARONS = "macarons"
    PURPLE_PASSION = "purple-passion"
    ROMA = "roma"
    ROMANTIC = "romantic"
    SHINE = "shine"
    VINTAGE = "vintage"
    WALDEN = "walden"
    WESTEROS = "westeros"
    WONDERLAND = "wonderland"


class _GeoType:
    SCATTER = "scatter"
    EFFECT_SCATTER = "effectScatter"
    HEATMAP = "heatmap"
    LINES = "lines"


class _BMapType:
    # BMap Control location
    ANCHOR_TOP_LEFT = 0
    ANCHOR_TOP_RIGHT = 1
    ANCHOR_BOTTOM_LEFT = 2
    ANCHOR_BOTTOM_RIGHT = 3

    # BMap Navigation Control Type
    NAVIGATION_CONTROL_LARGE = 0
    NAVIGATION_CONTROL_SMALL = 1
    NAVIGATION_CONTROL_PAN = 2
    NAVIGATION_CONTROL_ZOOM = 3

    # BMap Maptype Control Type
    MAPTYPE_CONTROL_HORIZONTAL = 0
    MAPTYPE_CONTROL_DROPDOWN = 1
    MAPTYPE_CONTROL_MAP = 2


class _NotebookType:
    JUPYTER_NOTEBOOK = "jupyter_notebook"
    JUPYTER_LAB = "jupyter_lab"
    NTERACT = "nteract"
    ZEPPELIN = "zeppelin"


class _OnlineHost:
    DEFAULT_HOST = "https://assets.pyecharts.org/assets/"
    NOTEBOOK_HOST = "http://localhost:8888/nbextensions/assets/"


RenderType = _RenderType()
FileType = _FileType()
SymbolType = _SymbolType()
ChartType = _ChartType
ThemeType = _ThemeType()
GeoType = _GeoType()
BMapType = _BMapType
NotebookType = _NotebookType()
OnlineHostType = _OnlineHost()


class _CurrentConfig:
    PAGE_TITLE = "Awesome-pyecharts"
    ONLINE_HOST = OnlineHostType.DEFAULT_HOST
    NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
    GLOBAL_ENV = Environment(
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
        loader=FileSystemLoader(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)), "render", "templates"
            )
        ),
    )


CurrentConfig = _CurrentConfig()
