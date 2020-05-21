# Compute satellite orbits
# Compute station visibility
#
# Import the library

from czml3 import Document, Packet, Preamble
from czml3.properties import Clock
from czml3.types import IntervalValue, TimeInterval

from .CzmlUtils import add_groundstation


class ScenarioCzml:
    def __init__(self, start, end, name=None, version="1.0"):
        self.start = start
        self.end = end
        self.name = name
        self.version = version
        self.ground_stations = None
        self.current_time = None
        self.clock_multipler = 60
        self.content = []

    def set_time(self, start, end):
        """Set mission time frame"""
        self.start = start
        self.end = end

    def set_groundstations(self, ground_stations):
        self.ground_stations = ground_stations

    def add_content(self, packets):
        """Generic method to add czml packets"""
        if isinstance(packets, Packet):
            self.content.append(packets)
        else:
            [self.content.append(p) for p in packets.dump()]

    def sef_clock_multipler(self, mult):
        """Set the clock multipler"""
        self.clock_multipler = mult

    def set_clock_current_time(self, current_time):
        """Set the clock time """
        self.current_time = current_time

    def create_document(self, filename):
        """Create the CZML document appending the different packets"""
        packets = []

        if self.current_time is None:
            self.current_time = self.start.str()

        preamble = Preamble(
            version=self.version,
            name=self.name,
            clock=IntervalValue(
                start=self.start.str(),
                end=self.end.str(),
                value=Clock(
                    currentTime=self.current_time, multiplier=self.clock_multipler
                ),
            ),
        )
        packets.append(preamble)

        # Create and append the document packet
        packet1 = Packet()
        packets.append(packet1)

        [packets.append(c) for c in self.content]

        # Create and append satellites events packets
        if self.ground_stations:
            availability_interval = TimeInterval(
                start=self.start.str(), end=self.end.str()
            )
            for ground_station in self.ground_stations:
                station_name = ground_station.name
                sta_car_pos = ground_station.to_czml()
                packet = add_groundstation(
                    station_name, sta_car_pos, availability_interval
                )
                packets.append(packet)

        # Initialize a document
        doc = Document(packets)

        # Write the CZML document to a file
        f = open(filename, "w")
        doc.dump(f)
        f.close()
