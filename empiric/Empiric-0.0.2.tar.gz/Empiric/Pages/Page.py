from flask import render_template

from Empiric.internal.Step import Step

class Page(Step):
  def __init__(self, m, template):
    super().__init__(m)
    self._template = template
  def run(self, **kwargs):
    return super().run(raiseError=True, **kwargs)
  def render(self, **kwargs):
    self._storeSettings(**kwargs)
    return render_template(self.template(), step=-1, **self.settings())
  def template(self):
    return self._template
