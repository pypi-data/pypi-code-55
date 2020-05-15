import datetime

from django.db.models import (
    DateTimeField, DecimalField, FloatField, IntegerField,
)
from django.db.models.expressions import OrderBy, When
from django.db.models.functions import (
    ACos, ASin, ATan, ATan2, Cast, Ceil, Coalesce, Cos, Cot, Degrees, Exp,
    Floor, Ln, Log, Radians, Round, Sin, Sqrt, StrIndex, Tan,
)


def coalesce(self, compiler, connection, **extra_context):
    # When coalescing a timestamptz column and a Python datetime, the datetime
    # must be cast to timestamptz (DateTimeField) to avoid "incompatible
    # COALESCE expressions: expected 'YYYY-MM-DDTHH:MM:SS'::TIMESTAMP to be of
    # type timestamptz, found type timestamp".
    if self.output_field.get_internal_type() == 'DateTimeField':
        clone = self.copy()
        clone.set_source_expressions([
            Cast(expression, DateTimeField()) for expression in self.get_source_expressions()
        ])
        return super(Coalesce, clone).as_sql(compiler, connection, **extra_context)
    return self.as_sql(compiler, connection, **extra_context)


def float_cast(self, compiler, connection, **extra_context):
    # Most cockroachdb math functions require float arguments instead of
    # decimal or integer.
    clone = self.copy()
    clone.set_source_expressions([
        Cast(expression, FloatField()) if isinstance(expression.output_field, (DecimalField, IntegerField))
        else expression for expression in self.get_source_expressions()
    ])
    return clone.as_sql(compiler, connection, **extra_context)


def order_by(self, compiler, connection, **extra_context):
    # This can be removed when cockroachdb add support for NULL FIRST/LAST:
    # https://github.com/cockroachdb/cockroach/issues/6224
    # (or replaced with DatabaseFeatures.supports_order_by_nulls_modifier = False
    # in Django 3.1).
    template = None
    if self.nulls_last:
        template = '%(expression)s IS NULL, %(expression)s %(ordering)s'
    elif self.nulls_first:
        template = '%(expression)s IS NOT NULL, %(expression)s %(ordering)s'
    return self.as_sql(compiler, connection, template=template, **extra_context)


def when(self, compiler, connection, **extra_context):
    # As for coalesce(), cast datetimes to timestamptz.
    if isinstance(getattr(self.result, 'value', None), datetime.datetime):
        self.result = Cast(self.result, DateTimeField())
    return self.as_sql(compiler, connection, **extra_context)


def register_functions():
    math_funcs_needing_float_cast = (
        ACos, ASin, ATan, ATan2, Ceil, Cos, Cot, Degrees, Exp, Floor, Ln, Log,
        Radians, Round, Sin, Sqrt, Tan,
    )
    for func in math_funcs_needing_float_cast:
        func.as_cockroachdb = float_cast
    Coalesce.as_cockroachdb = coalesce
    OrderBy.as_cockroachdb = order_by
    StrIndex.as_cockroachdb = StrIndex.as_postgresql
    When.as_cockroachdb = when
