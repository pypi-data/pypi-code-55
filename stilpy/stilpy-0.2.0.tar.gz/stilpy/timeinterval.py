from datetime import datetime, timedelta
from typing import Union, Any, List, Optional
from functools import total_ordering

DATE_SEPARATORS = ["-", "/", "."]

@total_ordering
class TimeInterval:
    """
    Class representing a time interval between two moments.

    Attributes
    ----------
    start : datetime object or an empty str
        The starting point of the time interval. Default is an empty
        string.
    end : datetime object or an empty str
        The ending point of the time interval. Default is an empty
        string.
    duration : timedelta object or and empty str
        The duration of the time interval. If one of the limits
        (``start`` or ``end``) it's not set, the ``duration`` property
        will return an empty string.
    is_perfect : bool
        It will return ``False`` if neither ``start`` or ``end`` are empty
        strings. Othewise, ``True`` will be returned.
    """
    _EMPTY = ''
    _STR_DATETIME_ERRROR = '''
        Incorrect str date format. Must be: 'dd-mm-yyyy HH:MM:SS' or 
        'yyyy-mm-dd HH:MM:SS'. You can datetime use objects as well.
    '''
    _VALUE_ERROR = '''
        `start` and `end` attr must be datetime objects or formated
        strings.
    '''

    def __init__(
        self,
        *args,
        start: Union[datetime, str]='',
        end: Union[datetime, str]='',
        **kwargs: Optional[str]
    ) -> None:
        """

        Parameters
        ----------
        start : datetime object or str
            A datetime object representing the lower limit of the time
            interval. Default is an empty string.
            It accepts string formatted datetime like:

                * 'dd-mm-yyyy HH:MM:SS'
                * 'yyyy-mm-dd HH:MM:SS'

            Your can use dots, dashes and slashes as separators between
            the date elements and colons for the time elements.
            Hours goes from 00 to 23, minutes and seconds from 00 to 59.
        end : datetime object or str
            A datetime object representing the upper limit of the time
            interval. Default is an empty string.
            It accepts string formatted datetime like:

                * 'dd-mm-yyyy HH:MM:SS'
                * 'yyyy-mm-dd HH:MM:SS'

            Your can use dots, dashes and slashes as separators between
            the date elements and colons for the time elements.
            Hours goes from 00 to 23, minutes and seconds from 00 to 59.
        **kwargs : Any
            Any argument that must be an attribute of the 
            ``TimeInterval`` object. For example, a name, an age...

        Raises
        ------
        ValueError
            if the ``start`` or ``end`` argument passed to the constructor
            is not a datetime object, a valid formatted datetime or an empty
            string.
        """
        self.start = start
        self.end = end
        self._kwargs = kwargs
        self.__dict__.update(**kwargs)
        
    @property
    def start(self) -> datetime:
        """Returns the ``start`` property"""
        return self._start

    @start.setter
    def start(self, n_start: Union[datetime, str]) -> None:
        """Sets the ``start`` property to the n_start value."""
        if self._validate_datetime(n_start):
            pass
        elif self._validate_str(n_start):
            n_start = TimeInterval.str_to_datetime(n_start)
        else:
            raise ValueError(TimeInterval._VALUE_ERROR)

        # Checking that `star` is < than `end`

        self._start = n_start

    @property
    def end(self) -> datetime:
        """Returns the ``end`` property."""
        return self._end

    @end.setter
    def end(self, n_end: Union[datetime, str]) -> None:
        """Sets the ``end`` property to the ``n_end`` value."""
        if self._validate_datetime(n_end):
            pass
        elif self._validate_str(n_end):
            n_end = TimeInterval.str_to_datetime(n_end)
        else:
            raise ValueError(TimeInterval._STR_DATETIME_ERRROR)

        # self.start can't be bigger tan self.end
        if type(self.start) is str or type(n_end) is str:
            pass
        elif type(self.start) is datetime:
            if self.start > n_end:
                raise ValueError()
        
        self._end = n_end

    @property
    def duration(self) -> Union[timedelta, str]:
        """Returns the ``duration`` property."""
        try:
            return self.end - self.start
        except Exception:
            return TimeInterval._EMPTY

    @property
    def is_perfect(self) -> bool:
        """Returns ``True`` if the interval hasn't an empty ``start`` or ``end``.
        """
        if TimeInterval._EMPTY not in (self.start, self.end):
            return True
        else:
            return False

    def _validate_str(self, n_str_datetime: Any) -> bool:
        """Checks if a n_str_datetime is a str.
        
        Parameters
        ----------
        n_str_datetime: Any
            The value to check if it's a str.

        Returns
        -------
        bool
            True if n_str_datetime is a str. Otherway, 
            returns False.
        """
        if type(n_str_datetime) is str:
            return True
        else:
            return False

    def _validate_datetime(self, n_datetime: Any) -> bool:
        """Checks if a n_datetime is a datetime object.
        
        Parameters
        ----------
        n_datetime: Any
            The value to check if it's a datetime object or not.

        Returns
        -------
        bool
            True if n_datetime is a valid datetime object. Otherway, 
            returns False.
        """
        if type(n_datetime) is datetime:
            return True
        else:
            return False

    @staticmethod
    def str_to_datetime(n_datetime: str) -> Union[datetime, str]:
        """Tries to cast short string dates to ``date`` objet.
        
        Parameters
        ----------
        n_datetime: str
                A string format datetime. Date part accepts two 
                formats: 'yyyy-mm-dd' and 'dd-mm-yyyy'. You can use 3
                different separators: ``'-'``, ``'/'`` and ``'.'``.
                Time part only accepts one format: HH:MM:SS, using
                colons as separators. Hours goes from 00 to 23, minutes
                and seconds from 00 to 59.
                
        Returns
        -------
        datetime
              ``datetime`` object if ``n_datetime`` is a valid datetime
              formatted string.
        str
              if ``n_datetime`` is an empty string.
        
        Raises
        ------
        ValueError
            if the ``n_datetime`` argument passed to function is not a 
            valid formatted datetime or an empty string.
        """
        # Test if the str is empy
        if n_datetime == TimeInterval._EMPTY:
            return TimeInterval._EMPTY
        # Find the separator in the date element
        for sep in DATE_SEPARATORS:
            if sep in n_datetime:
                separator = sep
                break
        # Search if starts with year 
        if n_datetime.find(separator) == 4:
            casted_date = datetime.strptime(n_datetime, '%Y{s}%m{s}%d %H:%M:%S'.format(s=separator))
        # Search if date element ends with year
        elif n_datetime.split(' ')[0][::-1].find(separator) == 4:
            casted_date = datetime.strptime(n_datetime, '%d{s}%m{s}%Y %H:%M:%S'.format(s=separator))
        else:
            raise ValueError(TimeInterval._STR_DATETIME_ERRROR)
        return casted_date
    
    def __repr__(self) -> str:
        
        out_str = 'TimeInterval(start={!r}, end={!r}, duration={!r}'.format(
            self.start,
            self.end,
            self.duration
        )
        for k, v in self._kwargs.items():
            out_str += ', {}={!r}'.format(k, v)
        return out_str + ')'

    def __eq__(self, other: 'TimeInterval') -> bool:
        
        if (self.start == other.start) and (self.end == other.end):
            return True
        else:
            return self._eq_empty_prop(other)

    def __lt__(self, other: 'TimeInterval') -> bool:

        # if any start or end property is str, special lesser than
        # method is called
        if str in self._types_list(other):
            return self._lt_empty_prop(other)

        # else, the lesser than is revolved as usuall
        if (self.start < other.start) and (self.end < other.end):
            return True
        elif (self.start == other.start) and (self.end < other.end):
            return True
        elif (self.start < other.start) and (self.end >= other.end):
            return True
        else:
            return False

    def _types_list(self, other: 'TimeInterval') -> List[type]:
        """Returns a list with the start and end properties' types."""
        types = [
            type(self.start),
            type(self.end),
            type(other.start),
            type(other.end)
        ]
        return types

    def _eq_empty_prop(self, other: 'TimeInterval') -> bool:
        """Mangage == comparission between empty str and datetime."""
        case = self._find_comp_case(other)
        if case is 1:       # empty self.start
            return  True if self.end == other.end else False
        elif case is 3:     # empty self.end
            return True if self.start == other.start else False
        elif case is 5:     # empty other.start
            return True if self.end == other.end else False
        elif case is 9:     # empty other.end
            return True if self.start == other.start else False
        elif case is 10:    # emtpy self.start and other.end
            return True if self.end == other.start else False
        elif case is 8:     # empty self.end and other.start
            return True if self.start == other.end else False
        else:
            return False


    def _lt_empty_prop(self, other: 'TimeInterval') -> bool:
        """Mangage < comparission between empty str and datetime."""
        case = self._find_comp_case(other)
        if case is 6:       # empty self.start and other.start
            return True if self.end < other.end else False
        elif case is 12:    # empty self.end and other.end
            return True if self.start < other.start else False
        elif case is 1:     # empty self.start
            return True if self.end <= other.start else False
        elif case is 3:     # empty self.end
            return True if self.start < other.start else False
        elif case is 5:     # empty other.start
            if self.start == other.end:
                return False
            return True if self.start < other.end else False
        elif case is 9:     # empty other.end
            return True if self.start < other.start else False
        elif case is 10:    # emtpy self.start and other.end
            return True if self.end < other.start else False
        elif case is 8:     # empty self.end and other.start
            return True if self.start < other.end else False
        else:
            return False

    def _find_comp_case(self, other: 'TimeInterval') -> int:
        """Returns an int representing the case.
        
        It depences on the emtpy elements of the TimeIntervals.

        if your make a sum of the list elements in every case your have:
            empty self.start and other.start    =   6
            empty self.end and other.end        =   12
            empty self.start                    =   1
            empty self.end                      =   3
            empty other.start                   =   5
            empty other.end                     =   9
            emtpy self.start and other.end      =   10
            empty self.end and other.start      =   8
        """
        DT = 0
        case = 0
        types = [
            1 if type(self.start) is str else DT,
            3 if type(self.end) is str else DT,
            5 if type(other.start) is str else DT,
            9 if type(other.end) is str else DT
        ]

        for el in types:
            case += el
        return case