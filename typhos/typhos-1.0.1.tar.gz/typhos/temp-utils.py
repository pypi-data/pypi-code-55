def get_device_from_fake_class(cls):
    """
    Return the non-fake class, given a fake class

    That is::

        fake_cls = ophyd.sim.make_fake_device(cls)
        get_device_from_fake_class(fake_cls)  # -> cls

    Parameters
    ----------
    cls : type
        The fake class
    """
    bases = cls.__bases__
    if not bases or len(bases) != 1:
        raise ValueError('Not a fake class based on inheritance')

    actual_class, = bases

    if actual_class not in ophyd.sim.fake_device_cache:
        raise ValueError('Not a fake class (ophyd.sim does not know about it)')

    return actual_class


def is_fake_device_class(cls):
    """
    Is ``cls`` a fake device from :func:`ophyd.sim.make_fake_device`?
    """
    try:
        get_device_from_fake_class(cls)
    except ValueError:
        return False
    return True


def code_from_device_repr(device):
    """
    Return code to create a device from its :builtin:`repr` information

    Parameters
    ----------
    device : ophyd.Device
    """
    try:
        module = device.__module__
    except AttributeError:
        raise ValueError('Device class must be in a module') from None

    class_name = device.__class__.__name__
    if module == '__main__':
        raise ValueError('Device class must be in a module')

    cls = device.__class__
    is_fake = is_fake_device_class(cls)

    full_class_name = f'{module}.{class_name}'
    kwargs = '\n   '.join(f'{k}={v!r},' for k, v in device._repr_info())
    logger.debug('%r fully qualified Device class: %r', device.name,
                 full_class_name)
    if is_fake:
        actual_class = get_device_from_fake_class(cls)
        actual_name = f'{actual_class.__module__}.{actual_class.__name__}'
        logger.debug('%r fully qualified Device class is fake, based on: %r',
                     device.name, actual_class)
        return f'''\
import ophyd.sim
import pcdsutils

{actual_class.__name__} = pcdsutils.utils.import_helper({actual_name!r})
{class_name} = ophyd.sim.make_fake_device({actual_class.__name__})
{device.name} = {class_name}(
    {kwargs}
)
ophyd.sim.clear_fake_device({device.name})
'''

    return f'''\
import pcdsutils

{class_name} = pcdsutils.utils.import_helper({full_class_name!r})
{device.name} = {class_name}(
    {kwargs}
)
'''


def code_from_device(device):
    """
    Generate code required to load ``device`` in another process
    """
    is_fake = is_fake_device_class(device.__class__)
    if happi is None or not hasattr(device, 'md') or is_fake:
        return code_from_device_repr(device)

    happi_name = device.md.name
    return f'''\
import happi
from happi.loader import from_container
client = happi.Client.from_config()
md = client.find_device(name="{happi_name}")
{device.name} = from_container(md)
'''
