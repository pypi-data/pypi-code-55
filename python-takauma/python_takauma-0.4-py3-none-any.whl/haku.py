# -*- coding: utf-8 -*-

import functools
import glob
import importlib
import os
import re
import sys

import pkg_resources

from .hakemisto import Versiohakemisto


def etsi_versiot(kohde):
  '''
  Etsi levyltä kaikki versiot kohteen määrittelevästä moduulista, poimi
  vastaava kohde kustakin näistä ja palauta kohteet sanakirjana.
  (Versiohakemisto-muodossa).

  Python-tiedostoja etsitään nimellä <moduuli>-<versio>.py, missä
  moduuli vastaa `sys.modules[kohde.__module__].__file__`-arvoa
  (ilman .py-päätettä).

  Kunkin löytyneen moduulin sisältä poimitaan vastaava kohde
  `kohde.__qualname__`-määreen mukaisesti.

  Kullekin versioidulle, sanakirjaan lisättävälle kohteelle
  lisätään määre __versio__, joka sisältää vastaavan versionumeron.

  Args:
    kohde: luokka, funktio tai muu moduulitason kohde
  '''
  # Ohitetaan versioiden haku jo löytyneille versioille (rekursio).
  if '-' in kohde.__module__:
    return None

  # Kerätään levyltä löytyneet versiot sanakirjaan.
  versiot = {}

  # Etsi vanhempia versioita moduulin nimen mukaan.
  if kohde.__module__ not in sys.modules:
    return None
  tiedosto = sys.modules[kohde.__module__].__file__
  alku, loppu = os.path.splitext(tiedosto)
  for versioitu_tiedosto in glob.glob('-*'.join((alku, loppu))):
    versionumero = pkg_resources.parse_version(re.sub(
      rf'-(.*){loppu}', r'\1', versioitu_tiedosto.replace(alku, '')
    ))
    nimi = '-'.join((kohde.__module__, str(versionumero)))

    try:
      # Käytetään mahdollista jo aiemmin ladattua moduulia.
      versioitu_moduuli = sys.modules[nimi]

    except KeyError:
      # Lataa versioidun moduulitiedoston sisältö;
      # ks. https://docs.python.org/3.6/library/importlib.html, kpl 31.5.6.3.
      spec = importlib.util.spec_from_file_location(
        nimi, versioitu_tiedosto,
      )
      versioitu_moduuli = importlib.util.module_from_spec(spec)
      try:
        spec.loader.exec_module(versioitu_moduuli)
      except: # pylint: disable=bare-except
        # Ohitetaan versio, mikäli sen lataus epäonnistuu.
        continue
      # Tallenna luotu moduuli.
      sys.modules[nimi] = versioitu_moduuli
      # except KeyError

    # Poimi versioitu kohde samasta `__qualname__`-polusta kuin
    # ajantasaisessa moduulissa.
    # Aseta versionumero löytyneen kohteen tietoihin.
    # Ohita tämä versio, ellei kohdetta löydy.
    try:
      versioitu_kohde = functools.reduce(
        getattr, kohde.__qualname__.split('.'), versioitu_moduuli
      )
    except AttributeError:
      pass
    else:
      versioitu_kohde.__versio__ = versionumero
      versiot[versionumero] = versioitu_kohde
    # for versioitu_tiedosto

  # Muodosta ja palauta versiohakemisto.
  jarjestetyt_versionumerot = sorted(versiot)
  return Versiohakemisto((*zip(
    jarjestetyt_versionumerot,
    map(versiot.get, jarjestetyt_versionumerot)
  ), (
    # Lisää nykyinen versio.
    kohde.__versio__ or pkg_resources.parse_version('0'), kohde,
  )))
  # def etsi_versiot
