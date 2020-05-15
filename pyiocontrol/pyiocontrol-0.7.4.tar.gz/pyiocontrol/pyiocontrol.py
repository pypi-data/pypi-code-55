import time, json, threading
from requests import get

_DEFAULT_INTERVAL_READ = 5000
_DEFAULT_INTERVAL_WRITE = 3000
_MAX_TRIES = 10

OK = 0
httpOk = 200
emptyBoard = 604
nothingToWrite = 606
intervalError = 702
invalidResponse = 703
invalidNameReq = 1002
invalidName = 1003
val_index = 0
pending = 1
num_tries = 2
fl_index = 3


class Panel:

    __name = ""
    __key = None
    __read_interval = _DEFAULT_INTERVAL_READ
    __write_interval = _DEFAULT_INTERVAL_WRITE
    __read_timestamp = 0
    __write_timestamp = 0
    __devices = 1
    __objCount = []
    __panel_exists = True
    __created = False
    __panel_size = 0
    localUpdated = False
    siteUpdated = False

    __state = {}#{"myInt": [42, False, _MAX_TRIES], "myfloat": [3.14, False, _MAX_TRIES]}


    def __init__(self, name, key = None):

        self.__name = name
        self.__key = 0

        if key is not None:

            self.__key = key

        self.__objCount.append('1')

        error = self.readUpdate()

        if error != 0:
            raise ValueError('запрос на сайт вернул ошибку:', error)

        self.__created = True


    def __getattr__(self, item):

        if item.startswith("_"):
            super(Panel, self).__getattr__(item)

        else:
            self.readUpdate()
            try:
                val = self.__state.get(item)[val_index]

            except TypeError:
                raise TypeError('переменной с таким именем нет в панели')

            return val


    def __setattr__(self, item, new_val):

        if item.startswith("_") or item == "localUpdated" or item == "siteUpdated":
            super(Panel, self).__setattr__(item, new_val)

        #print(new_val, self.__state[item][val_index])
        elif new_val != self.__state[item][val_index]:

            #print(new_val, self.__state[item][val_index])
            try:

                self.__state[item][val_index] = new_val
                self.__state[item][pending] = True
                self.writeUpdate()

            except KeyError:

                raise KeyError('переменной с таким именем нет в панели')


    def readUpdate(self):

        currentTime = self.__millis()

        if not self.__panel_exists:

            return invalidName


        if abs(currentTime - self.__read_timestamp) > self.__read_interval\
                or self.__created == False:

            #print("updated")
            self.__read_timestamp = self.__millis()

            req = "https://iocontrol.ru/api/readDataAll/" + self.__name + "/0"

            #print(req)
            response = get(req)
                       #"https://iocontrol.ru/api/readDataAll/"
                       #+ self.__name
                       #+ "/0"
                       #)

        else:

            self.localUpdated = False
            return intervalError


        if response.status_code != httpOk:

            return response.status_code


        j = json.loads(response.text)

        check = j["check"]

        if not check:

            m = j["message"]

            if m == invalidName or m == invalidNameReq:

                self.__panel_exsists = False
                raise NameError('панель с таким именем не существует')

            return m

        self.__panel_size = j["countVariable"]

        if self.__panel_size == 0:

            return emptyBoard

        multiplier = self.__devices * len(self.__objCount)
        self.__read_interval = j["mTimeR"] * multiplier
        self.__write_interval = j["mTimeW"] * multiplier

        for data in j["data"]:

            # Sorry
            f = data["type"] == "float"

            temp = []

            if f:
                temp.append(float(data["value"]))
            else:
                temp.append(data["value"])

            temp.append(False)
            temp.append(_MAX_TRIES)

            if f:
                s = data["value"]
                x = s[s.find('.') + 1:]
                #print(len(x))
                temp.append(len(x))
            self.__state[data["variable"]] = temp

        self.localUpdated = True

        return OK


    def writeUpdate(self):

        currentTime = self.__millis()

        if abs(currentTime - self.__write_timestamp) < self.__write_interval:
            self.siteUpdated = False
            return intervalError

        #print("test")
        self.__write_timestamp = self.__millis()
        req = "https://iocontrol.ru/api/sendDataAll/" + str(self.__name)\
                + "/" + str(self.__key) + "/"

        writeFlag = False

        for k in self.__state:

            if self.__state[k][pending] == True:
                if self.__state[k][val_index] == True:
                    self.__state[k][val_index] = 1
                writeFlag = True
                req += str(k) + ":" + str(self.__state[k][val_index]) + ","
                #self.__state[k][num_tries] = False

        if writeFlag:

            threading.Timer(self.__write_interval / 1000, self.writeUpdate).start()
#           print(req)
            ####
#           for k in self.__state:
#               self.__state[k][pending] = False
            ####

            resp = get(req)

            if resp.status_code != httpOk:

                return resp.status_code

            j = json.loads(resp.text)

            if j["check"] == False:
                return j["message"]

            data = j["data"]
            failed_flag = False

            for k in data:

                if data[k] == True:
                    #print(data[k])

                    self.__state[k][pending] = False

                else:

                    falied_flag = True
                    self.__state[k][num_tries] -= 1

                if self.__state[k][num_tries] == 0:

                    self.__state[k][num_tries] = _MAX_TRIES
                    self.__state[k][pending] = False

            #if failed_flag == False:
            self.siteUpdated = True

            return OK
        else:
            return nothingToWrite


    def __millis(self):

        return int(round(time.time() * 1000))


    def setDeviceCountOnIP(self, num):

        self.__devices = num
        self.readUpdate()
