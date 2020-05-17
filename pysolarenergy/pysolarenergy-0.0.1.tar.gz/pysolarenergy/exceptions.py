"""Exceptions for SolarEnergy."""


class SolarEnergyError(Exception):
    """Generic Inverter exception."""
    pass


class SolarEnergyConnectionError(SolarEnergyError):
    """Inverter connection exception."""
    pass


class SolarEnergyTimeoutError(SolarEnergyConnectionError):
    """Inverter connection timeout"""
    pass


class SolarEnergyClientError(SolarEnergyConnectionError):
    """Inverter ClientError"""
    pass


class SolarEnergyResponseError(SolarEnergyError):
    """IPP response exception."""
    pass


class SolarEnergyParseError(SolarEnergyResponseError):
    """Inverter parse exception."""
    pass


class SolarEnergyContentTypeError(SolarEnergyResponseError):
    """Inverter parse exception."""
    pass


class SolarEnergyAttributeError(SolarEnergyResponseError):
    """Inverter parse exception."""
    pass
