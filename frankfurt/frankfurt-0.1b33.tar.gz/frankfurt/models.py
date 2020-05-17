import dataclasses

from typing import Tuple, Type, Dict, Any, List, Optional

from .fields import BaseField, ForeignKeyField


@dataclasses.dataclass
class Meta:
    name: str

    abstract : bool = False

    table_name : str = dataclasses.field(init=False)

    fields : Dict[str, BaseField] = dataclasses.field(
        default_factory=dict
    )

    unique_fields : List[str] = dataclasses.field(
        default_factory=list
    )

    db: Optional = None

    primary_key : List[str] = dataclasses.field(
        default_factory=list
    )

    polymorphic_bases : List[str] = dataclasses.field(
        default_factory=list
    )

    polymorphic_on : Optional[str] = None

    polymorphic_identity : Optional[Any] = None

    def __post_init__(self):
        self.table_name = self.name.lower()

    @property
    def depends(self):
        # Return a list of methods that should be created first.

        deps = []

        for field_ in self.fields.values():
            if isinstance(field_, ForeignKeyField):
                deps.append(field_.to_field.model)

        return deps

    def extend_from_model(self, Meta):

        # Set the db.
        if hasattr(Meta, 'db'):
            self.db = Meta.db

        # Change the abstract.
        self.abstract = getattr(Meta, "abstract", self.abstract)

        # Change the table name.
        if hasattr(Meta, 'table_name'):
            self.table_name = Meta.table_name

        # Update the polymorphic information
        if hasattr(Meta, 'polymorphic_identity'):
            self.polymorphic_identity = Meta.polymorphic_identity

        if hasattr(Meta, 'polymorphic_on'):
            self.polymorphic_on = Meta.polymorphic_on


class ModelType(type):

    # Properties in the type
    @property
    def table_name(cls):
        return cls._meta.table_name

    def __new__(cls, name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):

        # Start with a fresh meta.
        meta = Meta(name)

        # Extract some information from bases.
        for base in bases:
            if hasattr(base, '_meta'):

                # Copy the reference to a database.
                meta.db = base._meta.db

                # Copy fields.
                for field_name, field in base._meta.fields.items():
                    meta.fields[field_name] = field.copy()

                    # Check if field is unique.
                    if field.unique:
                        meta.unique_fields.append(field_name)

                # Extract the polymorphic_on property.
                meta.polymorphic_on = base._meta.polymorphic_on
                meta.polymorphic_bases = base._meta.polymorphic_bases[:]

        if "Meta" in attrs:
            meta.extend_from_model(attrs["Meta"])

        # Extend the polymorphic bases
        if meta.polymorphic_on is not None:
            meta.polymorphic_bases.append(meta.table_name)

        # Append the fields defined in the model.
        for fname, value in attrs.items():
            if isinstance(value, BaseField):
                meta.fields[fname] = value

        # Detect the primary key from the fields.
        for fname, field in meta.fields.items():
            if field.primary_key:
                meta.primary_key.append(fname)

        # Modify the primary keys in case of a polymorphic base.
        if meta.polymorphic_on in meta.fields:
            if meta.table_name != meta.polymorphic_bases[0]:
                for fname in meta.primary_key:
                    meta.fields[fname] = ForeignKeyField(
                        to=f'{meta.polymorphic_bases[0]}.{fname}',
                        primary_key=True
                    )

        # Append the meta information to the class.
        attrs["_meta"] = meta

        model = super().__new__(cls, name, bases, attrs)

        # Add a reference for the fields.
        for field in meta.fields.values():
            field.model = model

        return model

    def from_record(cls, record):
        return cls(**record)


class Model(metaclass=ModelType):
    def __init__(self, **kwargs):

        # Save the value of the fields in this dict
        self._data_default = {}
        self._data = {}

        # Check for the kwargs in the fields.
        for name, value in kwargs.items():
            self._set_data(name, value)

        # Continue with default values.
        for name, field in self._meta.fields.items():
            if name not in self._data:
                if field.has_default:
                    self._set_data_default(name, field.default)

        # Check for not nulls (or maybe types?)
        for name, field in self._meta.fields.items():
            msg = f"Field {name} cannot be null (None)"

            if name in self._data:
                if field.not_null and self._data[name] is None:
                    raise TypeError(msg)
            elif name in self._data_default:
                if field.not_null and self._data_default[name] is None:
                    raise TypeError(msg)

    def __repr__(self):
        return f'<{self.__class__.__name__} />'

    def _set_data(self, name, value):
        if name not in self._meta.fields:
            raise TypeError(f"Model has no field {name}.")

        # Assert the type for this field.
        try:
            self._meta.fields[name].assert_type(value)
            self._data[name] = value
        except TypeError as e:
            msg = f"Field {name} can't accept value {value}: {str(e).lower()}"
            raise TypeError(msg)

    def _set_data_default(self, name, value):
        try:
            self._meta.fields[name].assert_type(value)
            self._data_default[name] = value
        except TypeError as e:
            msg = f"Field {name} can't accept value {value}: {str(e).lower()}"
            raise TypeError(msg)

    def __contains__(self, key):
        return (key in self._data) or (key in self._data_default)

    def __setitem__(self, key : str, value):
        if key not in self._meta.fields:
            msg = "Model {} has not field {}.".format(self._meta.name, key)
            raise KeyError(msg)

        self._data[key] = value

        if key in self._data_default:
            del self._data_default[key]

    def __getitem__(self, key : str):
        if key not in self._meta.fields:
            msg = "Model {} has not field {}.".format(self._meta.name, key)
            raise KeyError(msg)

        if key in self._data:
            return self._data[key]

        if key in self._data_default:
            return self._data_default[key]

        raise KeyError("Field {} has no value.".format(key))

    def _update_data(self, **kwargs):
        # Update the inner data from a record.

        if not set(kwargs).issubset(self._meta.fields):
            raise TypeError("Some arguments are not defined in the model.", kwargs)

        for name, value in kwargs.items():

            if name in self._meta.fields:
                self._data[name] = value

                if name in self._data_default:
                    del self._data_default[name]

        return self


class DeleteMixin:
    async def delete(self, sess):
        await sess.delete(self)


class UpdateMixin:
    async def update(self, sess):
        # Update a row in the database.
        return await sess.update(self)


class CreateMixin:
    @classmethod
    async def create(cls, db, **kwargs):
        # Create a row in the database.
        return await db.insert(cls(**kwargs))


class InsertMixin:
    async def insert(self, sess):
        # Insert a row in the database.
        return await sess.insert(self)
