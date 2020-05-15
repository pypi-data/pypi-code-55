import TareasCSVToBD
from polical import SendTaskToTrello
import SimpleIcsToCSV
from polical import configuration
users = configuration.load_config_file("polical.yaml")
filename = configuration.get_file_location("mycalendar.ics")
SimpleIcsToCSV.addEvent(SimpleIcsToCSV.findHeader(filename),filename)
for user in users.keys():
    #SimpleIcsToCSV.convertICStoCSV(users[user]['calendar_url'])
    TareasCSVToBD.LoadCSVTasktoDB(user, users[user])
    SendTaskToTrello.SendTaskToTrello(user, users[user])
