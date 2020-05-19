"""
This program shows a windows notification with information of your saved wifi networks
"""
import subprocess
from win10toast import ToastNotifier


a = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', 'backslashreplace').split('\n')
a = [i.split(":")[1][1:-1] for i in a if "Perfil de todos los usuarios" in i]
listOfssid = []
listOfpasswords = []
wifi_dict = {}


def analyse_wifi():
    for i in a:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])\
            .decode('utf-8', 'backslashreplace').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Contenido de la clave" in b]

        try:
            # print("{:<30}|  {:<}".format(i, results[0]))
            listOfssid.append(i)
            listOfpasswords.append(results[0])
        except IndexError:
            print("{:<30}|  {:<}".format(i, ""))

    zipObj = zip(listOfssid, listOfpasswords)
    wifi_dict = dict(zipObj)
    return wifi_dict


# print(analyse_wifi())#This function return a dict with the SSIDs and Passwords.
msg = ''
for key, value in analyse_wifi().items():
    msg += (str(key)+' : '+str(value)+'\n')  # Saving the dict on a printable variable

toast = ToastNotifier()
toast.show_toast("Tus Redes Wifi Guardadas son: ", msg, icon_path=None, duration=20)
