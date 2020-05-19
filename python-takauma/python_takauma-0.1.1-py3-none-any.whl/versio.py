# -*- coding: utf-8 -*-

import functools
import os
import sys

import pkg_resources


class Versio:
  '''
  Hae sen python-paketin versionumero, johon määrittelevä luokka
  sisältyy.

  Käytettävissä luokan määreenä esim. seuraavasti:
  class Foo:
    __versio__ = Versio()
    ...
  '''
  # pylint: disable=protected-access, not-an-iterable

  # Muodosta käännöksenaikaisesti luettelo paketeista
  # ja testeistä moduulin sisältymisestä niihin.
  # Vrt. https://stackoverflow.com/a/56032725
  def _jakelut():
    # pylint: disable=no-method-argument
    for jakelu in pkg_resources.working_set:
      try:
        # Hae asennetun paketin (pip install) tiedostoluettelo.
        # Python-moduuli (esim. .../site-packages/x/y/z.py) sisältyy
        # pakettiin, mikäli se esiintyy tiedostoluettelossa.
        testi = [
          os.path.normpath(os.path.join(jakelu.location, r.split(',')[0]))
          for r in jakelu.get_metadata_lines('RECORD')
        ].__contains__
      except FileNotFoundError:
        # Kehitystilassa (pip install -e) oleva paketti.
        # Python-moduuli (esim. ~/git/a/x/y/z.py) sisältyy pakettiin,
        # mikäli se sijaitsee paketin sisällä (~/git/a/).
        # Huomaa, että `partial`-kääre vaaditaan jakelun sitomiseksi
        # funktioon sen ulkopuolelta.
        testi = functools.partial(lambda t, j: os.path.commonpath((
          t, j.location
        )) == j.location, j=jakelu)
      yield (jakelu, testi)
    # for jakelu in pkg_resources.working_set
  _jakelut = list(_jakelut())

  # Käytetään globaalia välimuistisanakirjaa:
  # moduulin nimi -> versionumero.
  _valimuisti = {}

  @classmethod
  def moduulin_versio(cls, moduuli):
    '''
    Hae sen pip-paketin versionumero, johon annettu moduuli sisältyy.

    Raises:
      ValueError: moduuli ei sisälly mihinkään pip-pakettiin.

    Return:
      pkg_resources.packaging.version.Version
    '''
    # Haetaan välimuistista.
    try:
      return cls._valimuisti[moduuli]
    except KeyError:
      pass

    # Poimitaan versionumero moduulin polusta.
    if '-' in moduuli:
      cls._valimuisti[moduuli] = pkg_resources.parse_version(
        moduuli.split('-')[-1]
      )
      return cls._valimuisti[moduuli]

    # Otetaan moduulin tiedostopolku.
    try:
      tiedosto = sys.modules[moduuli].__file__
    except KeyError:
      return None

    # Haetaan asennetuista paketeista, tallennetaan välimuistiin.
    try:
      cls._valimuisti[moduuli] = pkg_resources.parse_version(next(
        jakelu for jakelu, testi in cls._jakelut if testi(tiedosto)
      )._get_version())
    except StopIteration:
      return None
    else:
      return cls._valimuisti[moduuli]
    # def moduulin_versio

  def __get__(self, instance, cls):
    return self.moduulin_versio(cls.__module__)
    # def __get__

  # class Versio
