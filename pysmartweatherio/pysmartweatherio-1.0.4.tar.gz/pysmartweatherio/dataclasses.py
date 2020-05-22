"""Defines the Data Classes used."""

class StationData:
    """A representation of all data available for a specific Station ID."""

    def __init__(self, data):
        self._air_density = data["air_density"]
        self._air_temperature = data["air_temperature"]
        self._brightness = data["brightness"]
        self._dew_point = data["dew_point"]
        self._feels_like = data["feels_like"]
        self._heat_index = data["heat_index"]
        self._lightning_strike_last_time = data["lightning_strike_last_time"]
        self._lightning_strike_last_distance = data["lightning_strike_last_distance"]
        self._lightning_strike_count = data["lightning_strike_count"]
        self._lightning_strike_count_last_3hr = data["lightning_strike_count_last_3hr"]
        self._precip_accum_last_1hr = data["precip_accum_last_1hr"]
        self._precip_accum_local_day = data["precip_accum_local_day"]
        self._precip_accum_local_yesterday = data["precip_accum_local_yesterday"]
        self._precip_rate = data["precip_rate"]
        self._precip_minutes_local_day = data["precip_minutes_local_day"]
        self._precip_minutes_local_yesterday = data["precip_minutes_local_yesterday"]
        self._relative_humidity = data["relative_humidity"]
        self._solar_radiation = data["solar_radiation"]
        self._station_pressure = data["station_pressure"]
        self._timestamp = data["timestamp"]
        self._uv = data["uv"]
        self._wind_avg = data["wind_avg"]
        self._wind_bearing = data["wind_bearing"]
        self._wind_chill = data["wind_chill"]
        self._wind_gust = data["wind_gust"]

    @property
    def air_density(self) -> float:
        """Return Air Density."""
        return self._air_density

    @property
    def air_temperature(self) -> float:
        """Return Outside Temperature."""
        return self._air_temperature

    @property
    def brightness(self) -> int:
        """Return Brightness in Lux."""
        return self._brightness

    @property
    def dew_point(self) -> float:
        """Return Outside Dewpoint."""
        return self._dew_point

    @property
    def feels_like(self) -> float:
        """Return Outside Feels Like Temp."""
        return self._feels_like

    @property
    def freezing(self) -> bool:
        """Return True if Freezing Outside."""
        if self.air_temperature < 0:
            return True

        return False

    @property
    def heat_index(self) -> float:
        """Return Outside Heat Index."""
        return self._heat_index

    @property
    def lightning(self) -> bool:
        """Return True if it is Lightning."""
        if self.lightning_strike_count > 0:
            return True

        return False
        
    @property
    def lightning_strike_last_time(self) -> str:
        """Return the date and time of last strike."""
        return self._lightning_strike_last_time

    @property
    def lightning_strike_last_distance(self) -> int:
        """Return the distance away of last strike."""
        return self._lightning_strike_last_distance

    @property
    def lightning_strike_count(self) -> int:
        """Return the daily strike count."""
        return self._lightning_strike_count

    @property
    def lightning_strike_count_last_3hr(self) -> int:
        """Return the strike count last 3hr."""
        return self._lightning_strike_count_last_3hr
        
    @property
    def precip_accum_last_1hr(self) -> float:
        """Return Precipition for the Last Hour."""
        return self._precip_accum_last_1hr
        
    @property
    def precip_accum_local_day(self) -> float:
        """Return Precipition for the Day."""
        return self._precip_accum_local_day
        
    @property
    def precip_accum_local_yesterday(self) -> float:
        """Return Precipition for Yesterday."""
        return self._precip_accum_local_yesterday

    @property
    def precip_rate(self) -> float:
        """Return current precipitaion rate."""
        return self._precip_rate
        
    @property
    def precip_minutes_local_day(self) -> int:
        """Return Precipition Minutes Today."""
        return self._precip_minutes_local_day
        
    @property
    def precip_minutes_local_yesterday(self) -> int:
        """Return Precipition Minutes Yesterday."""
        return self._precip_minutes_local_yesterday

    @property
    def relative_humidity(self) -> int:
        """Return relative Humidity."""
        return self._relative_humidity

    @property
    def raining(self) -> bool:
        """Return True if it is raining."""
        if self.precip_rate > 0:
            return True

        return False

    @property
    def solar_radiation(self) -> int:
        """Return Solar Radiation."""
        return self._solar_radiation
        
    @property
    def station_pressure(self) -> float:
        """Return Station Pressure."""
        return self._station_pressure
        
    @property
    def timestamp(self) -> str:
        """Return Data Timestamp."""
        return self._timestamp
        
    @property
    def uv(self) -> float:
        """Return UV Index."""
        return self._uv

    @property
    def wind_avg(self) -> float:
        """Return Wind Speed Average."""
        return self._wind_avg
        
    @property
    def wind_bearing(self) -> int:
        """Return Wind Bearing as Degree."""
        return self._wind_bearing

    @property
    def wind_chill(self) -> float:
        """Return Wind Chill."""
        return self._wind_chill

    @property
    def wind_gust(self) -> float:
        """Return Wind Gust Speed."""
        return self._wind_gust
        
    @property
    def wind_direction(self) -> str:
        """Return Wind Direction Symbol."""
        direction_array = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
        direction = direction_array[int((self._wind_bearing + 11.25) / 22.5)]
        return direction
