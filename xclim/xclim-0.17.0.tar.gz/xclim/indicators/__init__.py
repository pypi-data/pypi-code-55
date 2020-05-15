# -*- coding: utf-8 -*-
"""
Indicators module
=================

Indicators are then main tool xclim provides to compute climate indices. In contrast
to the function defined in `xclim.indices`, Indicators add a layer of heatlh checks
and metadata handling. Indicator objects are split into realms : atmos, land and
seaIce. The module also defines an additionnal virtual module : ICCLIM.
"""


def build_module(name, objs, doc="", source=None, mode="ignore"):
    """Create a module from imported objects.

    Parameters
    ----------
    name : str
      New module name.
    objs : dict
      Dictionary of the objects (or their name) to import into the module,
      keyed by the name they will take in the created module.
    doc : str
      Docstring of the new module.
    source : Module object
      Module where objects are defined if not explicitly given.
    mode : {'raise', 'warn', 'ignore'}
      How to deal with missing objects.


    Returns
    -------
    ModuleType
      A module built from a list of objects' name.

    """
    import sys
    import types
    import warnings
    import logging

    logging.captureWarnings(capture=True)

    try:
        out = types.ModuleType(name, doc)
    except TypeError:
        msg = "Module '{}' is not properly formatted".format(name)
        raise TypeError(msg)

    for key, obj in objs.items():
        if isinstance(obj, str) and source is not None:
            module_mappings = getattr(source, obj, None)
        else:
            module_mappings = obj

        if module_mappings is None:
            msg = "{} has not been implemented.".format(obj)
            if mode == "ignore":
                logging.info(msg)
            elif mode == "warn":
                warnings.warn(msg)
            elif mode == "raise":
                raise NotImplementedError(msg)
            else:
                msg = "{} is not a valid missing object behaviour".format(mode)
                raise AttributeError(msg)

        else:
            out.__dict__[key] = module_mappings
            try:
                module_mappings.__module__ = name
            except AttributeError:
                msg = "{} is not a function".format(module_mappings)
                raise AttributeError(msg)

    sys.modules[name] = out
    return out


def __build_icclim(mode="warn"):
    from xclim import indices
    from xclim.core.utils import wrapped_partial

    #  ['SD', 'SD1', 'SD5cm', 'SD50cm',

    # TODO : Complete mappings for ICCLIM indices
    mapping = {
        "TG": indices.tg_mean,
        "TX": indices.tx_mean,
        "TN": indices.tn_mean,
        "TG90p": indices.tg90p,
        "TG10p": indices.tg10p,
        "TGx": indices.tg_max,
        "TGn": indices.tg_min,
        "TX90p": indices.tx90p,
        "TX10p": indices.tx10p,
        "TXx": indices.tx_max,
        "TXn": indices.tx_min,
        "TN90p": indices.tn90p,
        "TN10p": indices.tn10p,
        "TNx": indices.tn_max,
        "TNn": indices.tn_min,
        "CSDI": indices.cold_spell_duration_index,
        "SU": indices.tx_days_above,
        "CSU": indices.maximum_consecutive_tx_days,
        "TR": indices.tropical_nights,
        "GD4": wrapped_partial(indices.growing_degree_days, thresh="4 degC"),
        "FD": indices.frost_days,
        "CFD": indices.consecutive_frost_days,
        "GSL": indices.growing_season_length,
        "ID": indices.ice_days,
        "HD17": wrapped_partial(indices.heating_degree_days, thresh="17 degC"),
        "CDD": indices.maximum_consecutive_dry_days,
        "CWD": indices.maximum_consecutive_wet_days,
        "PRCPTOT": indices.precip_accumulation,
        "RR1": indices.wetdays,
        "SDII": wrapped_partial(indices.daily_pr_intensity, thresh="1 mm/day"),
        "ETR": indices.extreme_temperature_range,
        "DTR": indices.daily_temperature_range,
        "vDTR": indices.daily_temperature_range_variability,
        "R10mm": wrapped_partial(indices.wetdays, thresh="10 mm/day"),
        "R20mm": wrapped_partial(indices.wetdays, thresh="20 mm/day"),
        "RX1day": indices.max_1day_precipitation_amount,
        "RX5day": wrapped_partial(indices.max_n_day_precipitation_amount, window=5),
        "WSDI": indices.warm_spell_duration_index,
        "R75p": wrapped_partial(indices.days_over_precip_thresh, thresh="1 mm/day"),
        "R95p": wrapped_partial(indices.days_over_precip_thresh, thresh="1 mm/day"),
        "R99p": wrapped_partial(indices.days_over_precip_thresh, thresh="1 mm/day"),
        "R75pTOT": wrapped_partial(
            indices.fraction_over_precip_thresh, thresh="1 mm/day"
        ),
        "R95pTOT": wrapped_partial(
            indices.fraction_over_precip_thresh, thresh="1 mm/day"
        ),
        "R99pTOT": wrapped_partial(
            indices.fraction_over_precip_thresh, thresh="1 mm/day"
        ),
        # 'SD': None,
        # 'SD1': None,
        # 'SD5cm': None,
        # 'SD50cm': None,
    }

    mod = build_module(
        "xclim.icclim",
        mapping,
        doc="""
            ==============
            ICCLIM indices
            ==============
            The European Climate Assessment & Dataset project (`ECAD`_) defines
            a set of 26 core climate indides. Those have been made accessible
            directly in xclim through their ECAD name for compatibility. Hoewever,
            the methods in this module are only wrappers around the corresponding
            methods of  `xclim.indices`. Note that none of the checks performed by
            the `xclim.utils.Indicator` class (like with `xclim.atmos` indicators)
            are performed in this module.

            .. _ECAD: https://www.ecad.eu/
            """,
        mode=mode,
    )
    return mod


ICCLIM = __build_icclim("ignore")
