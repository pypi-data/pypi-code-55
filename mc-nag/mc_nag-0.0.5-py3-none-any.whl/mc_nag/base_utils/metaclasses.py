"""Metaclasses to help with base class creation."""


class RequiredAttributeDefinitionMeta(type):
    """Metadata class to enforce required attributes on subclasses."""

    def __call__(cls, *args, **kwargs):
        """Execute check_required_attributes() when class is called."""
        class_object = type.__call__(cls, *args, **kwargs)
        class_object.check_required_attributes()
        return class_object
