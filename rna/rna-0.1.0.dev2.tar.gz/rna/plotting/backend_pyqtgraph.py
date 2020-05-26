"""
Use pyqtgraph for fast 3d plots especially.
pyqtgraphs GFViewWidget is used as a correlate to matplotlibs Axes
"""
import rna
import numpy as np
import sys
import pyqtgraph as pg
import pyqtgraph.opengl
import pyqtgraph.exporters


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'w')


def axes_dim(axes):
    return 3


global window, view
window, view = None, None
def gca(dim=None):
    if dim is None:
        dim = 3
    if dim != 3:
        raise NotImplementedError()
    global window, view
    if view is None:
        pg.mkQApp()
        window = pg.LayoutWidget()
        view = pg.opengl.GLViewWidget()
        view.setBackgroundColor('w')
        window.resize(800, 800)
    return view


def show():
    global window, view
    window.addWidget(view)
    window.show()

    if (sys.flags.interactive != 1) or not hasattr(pg.Qt.QtCore, 'PYQT_VERSION'):
        pg.Qt.QtGui.QApplication.instance().exec_()


def clear(axes):
    global window, view
    view.setParent(None)
    # window.removeWidget(view)
    view = None


def _save(path, **kwargs):
    axes = kwargs.get('axes', None)
    if axes is None:
        axes = gca()
    axes.grabFrameBuffer().save(path, **kwargs)
    # global window
    # exporter = pg.exporters.ImageExporter(window.plotItem)
    # exporter.parameters().update(kwargs)
    # exporter.export(path)


class GraphicsViewOverlay2D(pg.GraphicsView):
    """
    GraphicsView subclass that uses GLViewWidget as its canvas. 
    This allows 2D graphics to be overlaid on a 3D background.
    """
    def __init__(self, axes):
        """
        Args:
            axes (gl.GLViewWidget): view upon which to copy all events
        """
        self.glView = axes
        pg.GraphicsView.__init__(self, background=None)
        self.setStyleSheet("background: transparent")
        self.setViewport(self.glView)

    def mousePos(self, event):
        """
        Distribute mouse events to both widgets
        """
        pg.GraphicsView.mousePos(self, event)
        self.glView.mousePos(event)
        
    def paintEvent(self, event):
        """
        Distribute paint events to both widgets
        """
        self.glView.paintEvent(event)
        return pg.GraphicsView.paintEvent(self, event)
    
    def mousePressEvent(self, event):
        """
        Distribute mouse events to both widgets
        """
        pg.GraphicsView.mousePressEvent(self, event)
        self.glView.mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """
        Distribute mouse events to both widgets
        """
        pg.GraphicsView.mouseMoveEvent(self, event)
        self.glView.mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """
        Distribute mouse events to both widgets
        """
        pg.GraphicsView.mouseReleaseEvent(self, event)
        self.glView.mouseReleaseEvent(event)


def plot_array(*args, **kwargs):
    raise NotImplementedError()


def plot_mesh(vertices, faces, **kwargs):
    po = rna.plotting.PlotManager(kwargs)
    po.set_default('drawEdges', False)
    po.set_default('smooth', False)
    po.set_default('shader', None)
    scalars = po.pop('color', None)
    if scalars is None:
        scalars = [0] * len(faces)
    cmap, vmin, vmax = po.get_norm_args(
        vmin_default=min(scalars),
        vmax_default=max(scalars),
        cmap_default='viridis')

    scalars = np.array(scalars)
    scalars[scalars < vmin] = vmin
    scalars[scalars > vmax] = vmax
    norms = (scalars - vmin) / (vmax - vmin)

    color_map = get_cmap(cmap)
    colors = color_map.map(norms, mode='float')

    mesh_data = pg.opengl.MeshData(
            vertexes=np.array(vertices),
            faces=np.array(faces),
            faceColors=colors)
    artist = pg.opengl.GLMeshItem(
        meshdata=mesh_data,
        **po.plot_kwargs)
    artist.colors = colors
    artist.vmin = vmin
    artist.vmax = vmax
    artist.color_map = color_map
    artist.setGLOptions('opaque')
    
    po.axes.addItem(artist)
    return artist


def get_cmap(cm_name):
    """
    Use matplotlib conventions to retrieve a pg.ColorMap

    Examples:
        >>> import rna
        >>> rna.plotting.use('pyqtgraph')
        >>> cm = rna.plotting.backend.get_cmap('viridis')
    """
    import matplotlib.pyplot as plt
    pltMap = plt.get_cmap(cm_name)
    colors = pltMap.colors
    colors = [c + [1.] for c in colors]
    positions = np.linspace(0, 1, len(colors))
    cmap = pg.ColorMap(positions, colors)
    return cmap


def set_colorbar(axes, artist, label=None, position='right',
                 **kwargs):
    # Make a 2D color bar using the same ColorMap
    overlay_view = GraphicsViewOverlay2D(axes)
    kwargs['size'] = kwargs.pop('size', (20, 200))
    kwargs['offset'] = kwargs.pop('offset', (15, -25))
    colorbar_legend = Colorbar(artist, label=label, **kwargs)
    overlay_view.addItem(colorbar_legend)
    return overlay_view


class Colorbar(pg.GradientLegend):
    def __init__(self, artist, *args, **kwargs):
        self.label = kwargs.pop('label')
        self.format = kwargs.pop('format', '{0:.2f}')
        self.vmin, self.vmax = artist.vmin, artist.vmax
        ticks = kwargs.pop('ticks', np.linspace(self.vmin, self.vmax, 4))
        super(Colorbar, self).__init__(*args, **kwargs)
        color_map = artist.color_map
        self.setGradient(color_map.getGradient())
        self.set_tick_positions(ticks)

    def set_tick_positions(self, tick_positions):
        if self.vmin > min(tick_positions) or self.vmax < max(tick_positions):
            raise ValueError("tick positions must lie in (vmin, vmax)")
            
        self.setLabels(
            dict([(self.format.format(v), 1 / (self.vmax - self.vmin) * v - self.vmin / (self.vmax - self.vmin)) for v in tick_positions])
        )

    def paint(self, p, opt, widget):
        pg.UIGraphicsItem.paint(self, p, opt, widget)
        rect = self.boundingRect()   ## Boundaries of visible area in scene coords.
        unit = self.pixelSize()       ## Size of one view pixel in scene coords.
        if unit[0] is None:  
            return
        
        ## determine max width of all labels
        labelWidth = 0
        labelHeight = 0
        for k in self.labels:
            b = p.boundingRect(pg.Qt.QtCore.QRectF(0, 0, 0, 0), pg.Qt.QtCore.Qt.AlignLeft | pg.Qt.QtCore.Qt.AlignVCenter, str(k))
            labelWidth = max(labelWidth, b.width())
            labelHeight = max(labelHeight, b.height())

        b_tick = p.boundingRect(pg.Qt.QtCore.QRectF(0, 0, 0, 0), pg.Qt.QtCore.Qt.AlignCenter | pg.Qt.QtCore.Qt.AlignVCenter, '-')
        b_label = p.boundingRect(pg.Qt.QtCore.QRectF(0, 0, 0, 0), pg.Qt.QtCore.Qt.AlignCenter |
                pg.Qt.QtCore.Qt.AlignVCenter, str(self.label))
            
        labelWidth *= unit[0]
        labelHeight *= unit[1]
        
        textPadding = 2  # in px
        
        if self.offset[0] < 0:
            x3 = rect.right() + unit[0] * self.offset[0]
            x2 = x3 - labelWidth - unit[0]*textPadding*2
            x1 = x2 - unit[0] * self.size[0]
        else:
            x1 = rect.left() + unit[0] * self.offset[0]
            x2 = x1 + unit[0] * self.size[0]
            x3 = x2 + labelWidth + unit[0]*textPadding*2
        if self.offset[1] < 0:
            y2 = rect.top() - unit[1] * self.offset[1]
            y1 = y2 + unit[1] * self.size[1]
        else:
            y1 = rect.bottom() - unit[1] * self.offset[1]
            y2 = y1 - unit[1] * self.size[1]
        self.b = [x1,x2,x3,y1,y2,labelWidth]
        
        ## Have to scale painter so that text and gradients are correct size. Bleh.
        p.scale(unit[0], unit[1])
        
        ## Draw color bar
        self.gradient.setStart(0, y1/unit[1])
        self.gradient.setFinalStop(0, y2/unit[1])
        p.setBrush(self.gradient)
        rect = pg.Qt.QtCore.QRectF(
            pg.Qt.QtCore.QPointF(x1/unit[0], y1/unit[1]), 
            pg.Qt.QtCore.QPointF(x2/unit[0], y2/unit[1])
        )
        p.drawRect(rect)

        ## draw labels
        p.setPen(pg.Qt.QtGui.QPen(pg.Qt.QtGui.QColor(0,0,0)))
        tx = x2 + unit[0]*textPadding
        lh = labelHeight/unit[1]
        for k in self.labels:
            y = y1 + self.labels[k] * (y2-y1)
            p.drawText(pg.Qt.QtCore.QRectF(tx/unit[0] + b_tick.width(), y/unit[1] - lh/2.0, 1000, lh), pg.Qt.QtCore.Qt.AlignLeft | pg.Qt.QtCore.Qt.AlignVCenter, str(k))
            p.drawText(pg.Qt.QtCore.QRectF(x2, y/unit[1] - b_tick.height()/2.0 - 2,  # the -2 is a hack to move the ticks up
                                           b_tick.width(),
                                           b_tick.height()),
                                           pg.Qt.QtCore.Qt.AlignLeft | pg.Qt.QtCore.Qt.AlignVCenter, '-')
        p.save()
        p.translate(x3 + b_label.height(), y1 + 0.5 * (y2 - y1) - b_label.width() / 2)
        p.rotate(90)
        p.drawText(0., 0., str(self.label))
        p.restore()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
