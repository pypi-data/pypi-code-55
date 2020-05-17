import math

from Empiric.internal.Statistics import VISUALIZATION_TYPE
from Empiric.Pages.Page import Page

class TASK:
  DRAW_GEOMETRIES = 'DRAW_GEOMETRIES'
  TRANSFORM_GEOMETRIES = 'TRANSFORM_GEOMETRIES'

class PageMap(Page):
  def run(self, **settings):
    settings = {
      'task': TASK.DRAW_GEOMETRIES,
      'transformTranslate': False,
      'transformResize': True,
      'transformResizeNonUniform': False,
      'transformRotate': True,
      'geometries': [],
      'geometriesColor': 'RED',
      'drawColor': 'BLUE',
      'drawCount': None,
      'backgroundImageSize': {'width': 2560, 'height': 1600},
      'backgroundOpacity': .6,
      'waitAfterLastDraw': 2000,
      'waitBeforeNext': 1000,
      **settings,
    }
    if 'instruction' not in settings:
      if settings['task'] == TASK.DRAW_GEOMETRIES:
        if settings['drawCount'] == 1:
          settings['instruction'] = 'Draw one additional geometry'
        else:
          settings['instruction'] = 'Draw additional geometries'
      if settings['task'] == TASK.TRANSFORM_GEOMETRIES:
        settings['instruction'] = 'Transform the geometries'
    statistics = None
    if 'statistics' in settings and isinstance(settings['statistics'], str):
      statistics = {
        'title': settings['statistics'],
        'substatistics': [],
      }
      if settings['task'] == TASK.DRAW_GEOMETRIES:
        if settings['drawCount'] is None or settings['drawCount'] > 1:
          statistics['substatistics'].append({
            'key': 'newCountdrawnGeometriesCount',
            'title': 'Number of drawn geometries',
            'data': {
              'selector': 'geometries[*].type',
              'aggregateByPage': 'count',
              'defaultValue': 0,
            },
            'visualization': {
              'type': VISUALIZATION_TYPE.BOX_PLOT,
            },
          })
        statistics['substatistics'].append({
          'key': 'drawnGeometries',
          'title': 'Drawn geometries',
          'data': {
            'selector': 'geometries[*]',
            'aggregateByPage': 'collect',
          },
          'visualization': {
            'type': VISUALIZATION_TYPE.MAP,
            'backgroundImage': settings['backgroundImage'],
            'backgroundImageSize': settings['backgroundImageSize'],
          },
        })
      if settings['task'] == TASK.TRANSFORM_GEOMETRIES:
        statistics['substatistics'].append({
          'key': 'changed',
          'title': 'Number of changed geometries',
          'data': {
            'selector': {'translate': 'geometries[*].userTranslate', 'scale': 'geometries[*].userScale', 'rotate': 'geometries[*].userRotate'},
            'aggregateByPage': 'count',
            'defaultValue': {'translate': 0, 'scale': 0, 'rotate': 0},
          },
          'visualization': {
            'type': VISUALIZATION_TYPE.BOX_PLOT,
          },
        })
        if settings['transformTranslate']:
          statistics['substatistics'].append({
            'key': 'changedTranslate',
            'title': 'Translation',
            'data': {
              'selector': 'geometries[*]',
              'aggregateByKey': 'filename',
              'value': {'x': 'userTranslate[0]', 'y': 'userTranslate[1]'},
              'defaultValue': {'x': 0, 'y': 0},
            },
            'visualization': {
              'type': VISUALIZATION_TYPE.BOX_PLOT,
              'min': -5,
              'max': 5,
            },
          })
        if settings['transformResize']:
          statistics['substatistics'].append({
            'key': 'changedScale',
            'title': 'Resize',
            'data': {
              'selector': 'geometries[*]',
              'aggregateByKey': 'filename',
              'value': {'x': 'userScale[0]', 'y': 'userScale[1]'},
              'defaultValue': {'x': 1, 'y': 1},
            },
            'visualization': {
              'type': VISUALIZATION_TYPE.BOX_PLOT,
              'min': .7,
              'max': 1.3,
            },
          })
        if settings['transformRotate']:
          statistics['substatistics'].append({
            'key': 'changedRotate',
            'title': 'Rotate',
            'data': {
              'selector': 'geometries[*]',
              'aggregateByKey': 'filename',
              'value': 'userRotate',
              'defaultValue': 0,
            },
            'visualization': {
              'type': VISUALIZATION_TYPE.BOX_PLOT,
              'min': -math.pi / 10,
              'max': math.pi / 10,
            },
          })
    return super().run(defaultStatistics=statistics, **settings)
def pageMap(m, backgroundImage=None, **kwargs):
  if not backgroundImage:
    raise Exception('Please provide a background image')
  return PageMap(m, 'pageMap.html').run(backgroundImage=backgroundImage, **kwargs)
