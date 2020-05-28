from .utils import get_t2meta_cls


class BaseOptions:
    def __init__(self, changes):
        self.changes = changes or []

    def merge(self, super_opts):
        if super_opts:
            self.changes += super_opts.changes
        return self

    @classmethod
    def from_meta(cls, meta):
        if meta:
            kwargs = {k: v for k, v in meta.__dict__.items() if not k.startswith("_")}
        else:
            kwargs = {}
        return cls(**kwargs)


class OrderingOptionsMixin:
    def __init__(self, can_order_by, default_ordering):
        self.can_order_by = self._to_tuple(can_order_by)
        self.default_ordering = self._to_tuple(default_ordering)

        assert not (
            set(self._cleaned_names(self.default_ordering)) - set(self.can_order_by)
        )

    @classmethod
    def _to_tuple(cls, value):
        if value is None:
            value = tuple()
        elif isinstance(value, str):
            value = (value,)
        else:
            value = tuple(value)

        assert isinstance(value, tuple)
        assert all([isinstance(v, str) and v for v in value]) or not value
        assert len(value) == len(set(value))

        return value

    @classmethod
    def _cleaned_names(cls, ordering):
        return [name.replace("-", "") for name in ordering]

    def validate_ordering(self, ordering):
        return all(
            [item in self.can_order_by for item in self._cleaned_names(ordering)]
        )


class InputObjectOptions(BaseOptions):
    def __init__(
        self, abstract=False, changes=None, required=None, model=None, fields=None
    ):
        assert not fields or model
        super().__init__(changes)
        self.abstract = abstract
        self.required = required or {}
        self.model = model
        self.fields = None
        self.required_fields = None
        if not fields:
            return
        self.fields = []
        self.required_fields = []
        for name in fields:
            if name.startswith("*"):
                name = name[1:]
                self.required_fields.append(name)
            self.fields.append(name)

    def merge(self, super_opts):
        super().merge(super_opts)
        if not self.model and super_opts and super_opts.abstract:
            self.model = super_opts.model
        return self


class DjangoObjectTypeOptions(OrderingOptionsMixin, BaseOptions):
    def __init__(self, can_order_by=None, default_ordering=None, changes=None):
        BaseOptions.__init__(self, changes)
        OrderingOptionsMixin.__init__(self, can_order_by, default_ordering)


class QueriesOptions(BaseOptions):
    def __init__(self, enable_ordering_for=None, changes=None):
        super().__init__(changes)
        self.enable_ordering_for = enable_ordering_for or []
