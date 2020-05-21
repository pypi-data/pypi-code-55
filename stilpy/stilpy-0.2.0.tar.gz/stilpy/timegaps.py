
from typing import Union, Any, Iterable, Iterator, List, Tuple, Optional
from operator import itemgetter
from itertools import groupby
from datetime import timedelta

from stilpy.timeinterval import TimeInterval

dicts = List[dict]

class TimeGaps:
    """

    Class representing a collection for time interval objects.

    It's an iterator of `TimeInterval Objects`_.

    Attributes
    ----------
    grouper_tags : List of dicts
        A list containig a collection of dictionarys with the keys
        passed as ``grouped_by`` parameter and the values finded in
        the ``iterable`` that makes the different groups.
    grouped_intervals : List of TimeGaps iterators
        Returns time intervals separated by groups. For every group a
        ``TimeGaps`` iterator is made an stored in a ``list``. The groups are 
        created using the ``group_by`` argument passed in the instance.
        
    Raises
    ------
    StopIteration
        Raised when the ``__next__()`` method is called but there are no
        more records to read.
    AttributeError
        Raised when ``grouper_tags`` or ``grouped_intervals`` attribute is
        reasigned.
    """
    ERROR_ITERABLE = "it's not a supported iterable."

    def __init__(
        self, 
        iterable: Iterable,
        tag_loc: Union[str, int],
        i_tag: Any,
        f_tag: Any,
        dt_loc: Union[str, int], 
        *args: Optional[str],
        group_by: Optional[Any]=None
    ) -> None:
        """

        Parameters
        ----------
        iterable : iterable of iterables
            An iterable object that contains a ``list`` of items.
            Those items must be ``dicts`` or dictlike objects. Lists,
            tuples and objects with ``__dict__`` atribute are accepted as
            well. 
            Every item, must content the next items inside:

                1. A ``datetime`` object or a string format datetime
                2. A item that defines if the ``datetime`` object or string
                   that we just mentioned is an initial or a final time 
                   point of a time interval.
        tag_loc : str or int
            Where to find the tag that contains the value representing
            wich part of the interval defines each element. In a ``list``
            or a ``tuple`` can be an index. In a ``dict`` can be a key
            that reference the value.
        i_tag : Any
            The name of the initial time tag in the iterable. It's 
            needed to know if a specific element of the iterable is an
            initial time value. Default is ``'start'``.
        f_tag : Any
            The name of the final time tag in the iterable. It's needed
            to know if a specific element of the iterable is a final
            time value. Default is ``'end'``.
        dt_loc : str or int
            The location, inside each element of the iterable, of the
            datetime information.
        args : str, optional
            Any argument that will be an attribute of the TimeInterval.
            For example, a name, an age... This parameter expects the key,
            or the attribute, depending on the ``iterable`` that is 
            passed as first argument. Cannot be a ``int``, or a ``TypeError``
            will be raised.
        group_by : Any, optional
            The tags that you want to use for making the correct pairs
            between the diferent records of your ``iterable``. If it is 
            ``None``, the intervals will be made considering only the
            ``i_tag`` and the ``f_tag``.
            You can pass a ``list``, ``tuple`` or a single value. But every
            tag you pass must be contained in the iterables inside the
            main ``iterable``.

        Raises
        ------
        ValueError
            If the iterables inside the main ``iterable`` are not supported
            a ``ValueError`` will be raised.
        TypeError:
            When ``int`` types are passed to the ``args`` parameter as
            additional attributes for ``TimeInterval``.
        """
        self._tag_loc = tag_loc
        self._i_tag = i_tag
        self._f_tag = f_tag
        self._dt_loc = dt_loc
        self._args = args

        self._index = 0
     
        self._lis_of_dicts = self._to_list_of_dicts(iterable) 
        self._grouper_tags, self._groups = TimeGaps._create_groups(
            self._lis_of_dicts,
            group_by
        )
        self._intervals = sorted(self._list_intervals())

    @property
    def grouper_tags(self) -> dicts:
        """Return a ``list`` of dictionaries with the grouper tags.

        For example, if the group were made with ``'name'`` and ``'surname'``,
        this property will return something like:
        ``{'name': 'Jonh', 'surname': 'Smith', ...}``.
        """
        return self._grouper_tags
    
    @property
    def grouped_intervals(self) -> List['TimeGaps']:
        """Returns a ``list`` with a ``TimeGaps`` iterator for each group.

        If there are no groups, a single ``TimeGaps`` object will be
        returned, with the same intervals, properties and methods
        as the initial instance of ``TimeGaps``.
        """
        grouped = []
        for group in self._groups:
            grouped.append(TimeGaps(
                group, self._tag_loc, self._i_tag, self._f_tag,
                self._dt_loc, *self._args
            ))
        return grouped

    def total_duration(self, default: Any=None) -> Union[timedelta, Any]:
        """Returns the total duration of the ``TimeIntervals`` iterator. 
        
        If any ``TimeInterval`` object is imperfect (``start`` or 
        ``end`` atributte is empty `''`), the `default` ``argument``
        passed to the method will be returned.

        Parameters
        ----------
        default : Any, optional
            The value that will be returned if any ``TimeInterval``
            object in the ``TimeGaps`` iterator hasn't a valid 
            duration for the sum.

        Returns
        -------
        timedelta
            When every ``TimeInterval`` object in the ``TimeGaps``
            iterator has a valid ``duration`` atributte (that's a
            ``timedelta`` type) the method will return a ``timedelta``
            object representing the sum of every ``duration`` atributte
            in the ``TimeInterval`` objects.
        Any
            If the method can't reach the sum, it returns the value of
            the ``default`` parameter.
        """
        total = timedelta()
        for interval in self._intervals:
            if not interval.is_perfect:
                return default
            total += interval.duration
        return total

    def total_duration_anyway(self) -> timedelta:
        """Returns the total duration of the ``TimeIntervals`` iterator. 
        
        If any ``TimeInterval`` object is imperfect (``start`` or 
        ``end`` atributte is empty `''`) the duration of the others
        intervals will be returned.

        Returns
        -------
        timedelta
            When every ``TimeInterval`` object in the ``TimeGaps``
            iterator has a valid ``duration`` atributte (that's a
            ``timedelta`` type) the method will return a ``timedelta``
            object representing the sum of every ``duration`` atributte
            in the ``TimeInterval`` objects. If any timeinterval hasn't
            a valid duration, that interval will be ignored, but the 
            duration will be returned anyway, with the sum of the
            intervals that do have a duration.
        """
        total = timedelta()
        for interval in self._intervals:
            if interval.is_perfect:
                total += interval.duration
        return total
    
    def _to_list_of_dicts(self, iterable: Iterable) -> dicts:
        """Cast the iterable of iterables to a iterable of dicts.
        
        If the iterable inside the main iterable is not supported, it
        will raise an ``ValueError``
        """
        iterable = list(iterable)
        if len(iterable) <= 0:
            raise IndexError('Iterable length cant\'t be 0')
        if 'index' in dir(iterable[0]):
            return [{i: el for i, el in enumerate(el)} for el in iterable]
        elif 'items' in dir(iterable[0]):
            return iterable
        elif 'keys' in dir(iterable[0]):
            return [{k: el[k] for k in el.keys()} for el in iterable]
        elif '__dict__' in dir(iterable[0]):
            return [el.__dict__ for el in iterable]
        else:
            raise ValueError(type(iterable), self.ERROR_ITERABLE)
    
    @staticmethod
    def _create_groups(
        iterable: Iterable, group_by: Union[None, str, Iterable]
    ) -> Tuple[dicts, dicts]:
        """Creates groups with the different combinations."""
        group_tags = []
        groups = []
        
        if group_by is None:
            groups.append(iterable)
            return None, groups

        if type(group_by) in (str, int):
            grouper = itemgetter(group_by)
        else:
            grouper = itemgetter(*group_by)

        s_iter = sorted(iterable, key=grouper)
        for tag, group in groupby(s_iter, grouper):
            # If group_by is a str or a int tag, we avoid zip.
            if type(group_by) in (str, int):
                group_tag = {}
                group_tag[group_by] = tag
            else:
                group_tag = dict(zip(group_by, tag))
            group_tags.append(group_tag)
            groups.append(list(group))

        return group_tags, groups
    
    def _sort_iter(self, iterable: dicts) -> dicts:
        """Returns a sorted by datetime iterable."""
        return sorted(iterable, key=itemgetter(self._dt_loc))

    def _list_intervals(self) -> List['TimeInterval']:
        """Creates a list of intervals by groups"""
        intervals = []
        for group in self._groups:
            interval = list(self._intervalize(
                self._sort_iter(group))
            )
            intervals.extend(interval)
        return intervals

    def _intervalize(self, sorted_iter: dicts) -> Iterator['TimeInterval']:
        """Returns a list with of TimeIntervals objects.

        If there is an incomplete interval, y create an empty starting
        or ending interval
        """
        skip_loop = False

        # Compere every item with the next one to find his pair.
        for i, el in enumerate(sorted_iter):
            if skip_loop == True:
                skip_loop = False
                continue
            el1 = sorted_iter[i + 1] if (i + 1) < len(sorted_iter) else None

            # Creates a perfect pair interval if finds a proper initial
            # and final point. Else, an incomplete interval is created,
            # depending on wich limit is missiing, start or end.
            kwargs = {k: v for k, v in el.items() if k in self._args}
            if self._are_pair(el, el1):
                interval = TimeInterval(
                    start=el[self._dt_loc],
                    end=el1[self._dt_loc],
                    **kwargs
                )
                skip_loop = True
            elif self._is_start(el):
                interval = TimeInterval(start=el[self._dt_loc], **kwargs)
                skip_loop = False
            elif self._is_end(el):
                interval = TimeInterval(end=el[self._dt_loc], **kwargs)
                skip_loop = False
            yield interval

    def _are_pair(self, el1: dict, el2: Union[dict, None]) -> bool:
        """Return True if the first element is start and the second end"""
        if el2 is None:
            return False
        if self._is_start(el1) and self._is_end(el2):
            return True
        else:
            return False

    def _is_start(self, element: dict) -> bool:
        """True if is a start elemente, else False"""
        tag = element[self._tag_loc]
        return True if tag == self._i_tag else False

    def _is_end(self, element: dict) -> bool:
        """True if is a end elemente, else False"""
        tag = element[self._tag_loc]
        return True if tag == self._f_tag else False

    def __iter__(self) -> Iterator['TimeInterval']:
        return self

    def __next__(self) -> 'TimeInterval':
        if self._index >= len(self._intervals):
            raise StopIteration
        index = self._index
        self._index += 1
        return self._intervals[index]

    def __contains__(self, value: 'TimeInterval') -> bool:
        return value in self._intervals

    def __len__(self) -> int:
        return len(self._intervals)

    def __repr__(self) -> str:
        out = ''
        for i, interval in enumerate(self._intervals):
            end = ', ' if (i + 1) != len(self._intervals) else ''
            out += repr(interval) + end
        return 'TimeGaps({})'.format(out)