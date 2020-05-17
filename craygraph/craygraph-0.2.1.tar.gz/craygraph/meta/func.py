from inspect import signature, Parameter, Signature

__all__ = [
  'get_kwargs',
  'apply_with_kwargs',

  'signature_with_self'
]

def get_kwargs(func):
  results = list()
  for name, p in signature(func).parameters.items():
    if p.kind == Parameter.VAR_KEYWORD:
      return None
    elif p.kind != Parameter.POSITIONAL_ONLY and p.kind != Parameter.VAR_POSITIONAL:
      results.append(name)

  return results

def apply_with_kwargs(f, *args, **kwargs):
  accepted_kwargs = get_kwargs(f)

  if accepted_kwargs is None:
    return f(*args, **kwargs)

  else:
    passed_kwargs = dict()

    for k, v in kwargs.items():
      if k in accepted_kwargs:
        passed_kwargs[k] = v

    return f(*args, **passed_kwargs)

def signature_with_self(obj):
  sign = signature(obj)
  pretty_parameters = [Parameter('self', kind=Parameter.POSITIONAL_OR_KEYWORD)]
  pretty_parameters.extend(sign.parameters.values())

  return Signature(parameters=pretty_parameters, return_annotation=sign.return_annotation)