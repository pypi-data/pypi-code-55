"""Common utility functions for dealing with iterators."""

from typing import (
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

T = TypeVar("T")


def get_single_element(l: Sequence[T]) -> Optional[T]:
    """
    Return the element contained in a single-element list.

    Return None if the list is empty, and raise an exception if more than one
    element is present.
    """
    if not l:
        return None
    if len(l) == 1:
        return l[0]
    raise ValueError("Too many elements in list: {}".format(l))  # pragma: no cover


S = TypeVar("S")


def zip_strict(
    required_ts: Sequence[T], optional_ts: Sequence[T], ss: Sequence[S]
) -> List[Tuple[T, S]]:
    """Zip two lists, raising if they are of unequal length."""
    if len(ss) < len(required_ts):
        raise ValueError(
            "too few elements ({}) - expected at least {}".format(
                len(ss), len(required_ts)
            )
        )
    ts = [*required_ts, *optional_ts]
    if len(ss) > len(ts):
        raise ValueError(
            "too many elements ({}) - expected at most {}".format(len(ss), len(ts))
        )
    return list(zip(ts, ss))


def zip_strict_extra(
    t: T, required_ts: Sequence[T], optional_ts: Sequence[T], ss: Sequence[S]
) -> List[Tuple[T, S]]:
    """
    Zip two lists, raising if the second is shorter.

    If the first is shorter, extend it with copies of t.
    """
    return zip_strict(
        required_ts,
        list(optional_ts) + [t] * (len(ss) - len(required_ts) - len(optional_ts)),
        ss,
    )


def zip_strict_dict(
    required_ts: Mapping[str, T], optional_ts: Mapping[str, T], ss: Mapping[str, S]
) -> Dict[str, Tuple[T, S]]:
    """Zip two dictionaries, raising if they do not contain the same keys."""

    def show_if(msg: str, keys: Set[str]) -> Optional[str]:
        return msg.format(", ".join(keys)) if keys else None

    missing_keys = show_if("missing keys '{}'", set(required_ts) - set(ss))
    ts = {**required_ts, **optional_ts}
    unexpected_keys = show_if("unexpected keys '{}'", set(ss) - set(ts))
    if missing_keys or unexpected_keys:
        raise ValueError(
            "key mismatch - {}".format(
                ", ".join((msg for msg in (missing_keys, unexpected_keys) if msg))
            )
        )
    return {k: (ts[k], ss[k]) for k in ss}


def zip_strict_dict_extra(
    t: T,
    required_ts: Mapping[str, T],
    optional_ts: Mapping[str, T],
    ss: Mapping[str, S],
) -> Dict[str, Tuple[T, S]]:
    """
    Zip two dictionaries, raising if the first contains keys not present in the second.

    If the second contains keys not present in the first, extend the first with copies of t.
    """
    return zip_strict_dict(
        required_ts,
        {
            **optional_ts,
            **{k: t for k in ss if k not in required_ts and k not in optional_ts},
        },
        ss,
    )


ExceptionType = Union[Type[Exception], Tuple[Type[Exception], ...]]


def accumulate_errors_l(
    exception_t: ExceptionType, fn_elts: Iterator[Tuple[Callable[[S], T], S]]
) -> Tuple[List[Tuple[int, T]], List[Tuple[int, Exception]]]:
    """Apply a function, appending the result or the raised exception to a list."""
    results, errors = accumulate_errors_d(
        exception_t, {i: fn_elt for i, fn_elt in enumerate(fn_elts)}
    )
    return list(results.items()), list(errors.items())


K = TypeVar("K")


def accumulate_errors_d(
    exception_t: ExceptionType, fn_elts: Mapping[K, Tuple[Callable[[S], T], S]]
) -> Tuple[Dict[K, T], Dict[K, Exception]]:
    """Apply a function, adding the result or the raised exception to a dict."""
    results: Dict[K, T] = {}
    errors: Dict[K, Exception] = {}
    for key, (fn, elt) in fn_elts.items():
        try:
            results[key] = fn(elt)
        except exception_t as e:
            errors[key] = e
    return results, errors


def divide_list(fn: Callable[[T], bool], ts: Sequence[T]) -> Tuple[List[T], List[T]]:
    """Divide a list into elements that meet a predicate and those that don't."""
    predicate_met: List[T] = []
    predicate_not_met: List[T] = []
    for t in ts:
        if fn(t):
            predicate_met.append(t)
        else:
            predicate_not_met.append(t)
    return (predicate_met, predicate_not_met)
