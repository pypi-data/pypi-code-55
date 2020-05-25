# -*- coding: utf-8 -*-
'''
Moduulikohtainen, ajonaikaisesti laskettava määre.

Määreen nimi muodostetaan poistamalla argumenttina annetun
funktion nimen edestä mahdolliset alaviivat.

Huomaa, että määrettä ei voida teknisistä rajoitteista johtuen
asettaa samalla nimellä samaan moduuliin kuin toteuttava funktio.

Esim.

>>> import sys
>>> from mmaare import mmaare # tai: import mmaare
>>> import xyz
>>> ...
>>> # Asetetaan määre `f` käsillä olevaan moduuliin (__main__).
>>> @mmaare
>>> def __f(moduuli):
>>>  return ''.join(reversed(list(moduuli.__name__)))
>>>...
>>> # Asettaa määreen eri nimellä toiseen moduuliin.
>>> mmaare(__f.fget, nimi='__nimi_vaarinpain__', moduuli=xyz)
>>> ...
>>>  print(sys.modules['__main__'].f) # --> __niam__
>>>  print(xyz.__nimi_vaarinpain__) # --> zyx
'''

import functools
import sys


class _Py36:
  '''Python 3.6 -toteutus.

  Periytetään moduulin luokka, lisätään määre.
  '''
  # pylint: disable=no-member
  def __init__(self, *args, **kwargs):
    import types
    super().__init__(*args, **kwargs)
    if not isinstance(self.moduuli, types.ModuleType):
      # Asetetaan arvo sellaisenaan muille kuin `ModuleType`-olioille.
      # Tällaisten moduulien `__class__` ei salli asettamista.
      setattr(self.moduuli, self.nimi, self.__get__(self.moduuli))
      return
    self.moduuli.__class__ = functools.wraps(
      self.moduuli.__class__,
      updated=()
    )(type(
      '_Moduuli',
      (self.moduuli.__class__, ),
      {self.nimi: self}
    ))
    # def __init__

  def __get__(self, obj, cls=None):
    # Poimitaan olemassaoleva arvo, jos se on asetettu.
    try: return obj.__dict__[self.nimi]
    except KeyError: pass
    arvo = super().__get__(obj, cls)
    # Sijoitus `mappingproxy`-tyyppiseen kontekstisanakirjaan
    # aiheuttaa poikkeuksen. Ohitetaan arvon asetus.
    try: obj.__dict__[self.nimi] = arvo
    except TypeError: pass
    return arvo
    # def __get__

  # class _Py36


class _Py37:
  '''Python 3.7+ -toteutus.

  "Periytetään" `__getattr__`-funktio (ks. PEP 562).
  '''
  # pylint: disable=no-member

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    def __getattr__(avain):
      # pylint: disable=no-member, protected-access
      if avain == self.nimi:
        return self.__get__(self.moduuli)

      # Estetään rekursio samalla avaimella.
      # Muuten ne __getattr__-toteutukset
      # (esim. `celery.local.LazyModule`), jotka käyttävät
      # `ModuleType.__getattribute__`-metodia puuttuvien arvojen
      # hakemiseen, aiheuttavat päättymättömän rekursiosilmukan.
      if avain in __getattr__.__rekursio__:
        return self._ei_loydy(self.moduuli, avain)

      try:
        __getattr__.__rekursio__.add(avain)
        return __getattr__.__wrapped__(avain)
      finally:
        __getattr__.__rekursio__.remove(avain)
      # def __getattr__
    self.moduuli.__getattr__ = functools.wraps(getattr(
      self.moduuli,
      '__getattr__',
      functools.partial(self._ei_loydy, self.moduuli)
    ))(__getattr__)
    __getattr__.__rekursio__ = set()
    # def __init__

  @staticmethod
  def _ei_loydy(moduuli, avain):
    raise AttributeError(f'{moduuli.__name__}: {avain!r}')
    # def _ei_loydy

  # class _Py37


class mmaare(
  _Py36 if sys.version_info < (3, 7) else _Py37,
  property
):
  # pylint: disable=invalid-name

  def __new__(cls, *args, **kwargs):
    '''
    Sallitaan käyttö koristeena kahdella tavalla:

    @mmaare
    def f(m): ...

    @mmaare(nimi='def')
    def abc(m): ...
    '''
    if args:
      return super().__new__(cls, *args, **kwargs)
    else:
      return functools.partial(cls, **kwargs)
    # def __new__

  def __init__(self, fget, nimi=None, moduuli=None):
    self.nimi = nimi or fget.__name__.lstrip('_')
    self.moduuli = moduuli or sys.modules[fget.__module__]
    if (self.moduuli.__name__, self.nimi) == (fget.__module__, fget.__name__):
      raise ValueError('Määrettä ei voida asettaa samalla nimellä: {fget}')
    super().__init__(fget)
    # def __init__

  # class mmaare


# Sallitaan tämän moduulin köyttö sellaisenaan koristeena.
sys.modules[__name__].__class__ = functools.wraps(
  sys.modules[__name__].__class__,
  updated=()
)(type('mmaare', (
  sys.modules[__name__].__class__,
), {'__call__': mmaare}))
