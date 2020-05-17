from Empiric.internal.Step import Step

class Register(Step):
  pass

def register(m, valueFn, **kwargs):
  v = valueFn()
  r = Register(m)
  r.run(raiseError=False, value=v, **kwargs)
  result = r.save({'value': v})
  return result['value']
