# from django.conf import settings
from django.db.models.base import ModelBase


class BaseClassExporter():
    export_status = True
    export_mode = ['private', 'public']

    def return_field_value(self, field_name, field_value):
        return field_value


class ExporterInitialization(object):
    arr: dict = {}

    # def check_settings(self):
    #     try:
    #         settings.EXPORTAPP_ENABLE
    #     except AttributeError as e:
    #         printlog(e)

    def isreg(self, modelclass):
        res = False
        if modelclass in self.arr:
            res = True
        return res

    def reg(self, modeclass_x, incclass_y):
        # print('ExporterInitialization start')
        # self.check_settings()
        #
        if isinstance(modeclass_x, ModelBase):
            if self.isreg(modeclass_x):
                print('The model %s is already registered' % modeclass_x.__name__)
            else:
                try:
                    incclass_y.export_status
                except Exception:
                    message = 'Attr \'export_status\' not given in class %s' % incclass_y.__name__
                    print(message)
                else:
                    # registration class
                    self.arr[modeclass_x] = incclass_y()
                    # print('ExporterInitialization %s' % (self.arr[modeclass_x]))

        # printlog(self.arr)

    def list(self):
        # printlog(self.arr)
        return self.arr

    # def show(self):
    #     # printlog(self.arr)
    #     return self.arr


exporter = ExporterInitialization()
