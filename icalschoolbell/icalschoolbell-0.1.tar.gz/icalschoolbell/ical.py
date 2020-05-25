import json
from datetime import timedelta

from icalendar import Calendar

class ical():
    #in_file is ical location, out_file is json location
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file

    def parse_ical(self) :
        timetable = {}

        g = open(self.in_file, 'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk() :
            if component.name == "VEVENT" :
                try :
                    timetable[format(component.get('DTSTART').dt + timedelta(hours=10), "%d/%m/%Y")].append(
                        {'teacher' : component.get('DESCRIPTION').split('\n')[0][10 :],
                         'period' : component.get('DESCRIPTION').split('\n')[1][-1],
                         'start' : format(component.get('DTSTART').dt + timedelta(hours=10), "%H:%M:%S"),
                         'end' : format(component.get('DTEND').dt + timedelta(hours=10), "%H:%M:%S")})

                except :
                    timetable[format(component.get('DTSTART').dt + timedelta(hours=10), "%d/%m/%Y")] = []
                    timetable[format(component.get('DTSTART').dt + timedelta(hours=10), "%d/%m/%Y")].append(
                        {'teacher' : component.get('DESCRIPTION').split('\n')[0][10 :],
                         'period' : component.get('DESCRIPTION').split('\n')[1][-1],
                         'start' : format(component.get('DTSTART').dt + timedelta(hours=10), "%H:%M:%S"),
                         'end' : format(component.get('DTEND').dt + timedelta(hours=10), "%H:%M:%S")})

        g.close()

        with open(self.out_file, 'w') as outfile :
            json.dump(timetable, outfile)

    def getClasses(self, today):
        with open(self.out_file) as json_file :
            data = json.load(json_file)
            return data[today]

    def printClasses(self, today) :
        with open(self.out_file) as json_file :
            data = json.load(json_file)
            for i in range(0, len(data[today])) :
                print("Period: {}, Teacher: {}, Start: {}, End: {}".format(data[today][i]['period'],
                                                                           data[today][i]['teacher'],
                                                                           data[today][i]['start'],
                                                                           data[today][i]['end']))


