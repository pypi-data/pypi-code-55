import sys, os, logging, requests, copy
import pymysql
import re
import string
from datetime     import time, timedelta, datetime, tzinfo, date
from shared.utils import Utils

DF = "%Y-%m-%d"

class InstagramUtils(Utils):

  def init(self, conf_file_path, trace_enabled = False):
      Utils.init(self, conf_file_path, trace_enabled)
      self.logger = logging.getLogger(__name__)
      print('InstagramUtils inited logger')
      print(self.logger)

  # def old_init(self, conf_file_path, trace_enabled = False):
  #     Utils.init(self, conf_file_path, trace_enabled)
  #     log_name = self.conf.get("log_name", "root")
  #     print('InstagramUtils init log_name')
  #     print(log_name)
  #     self.logger = Utils.init_logger(self) # logging.getLogger(log_name)
  #     print('InstagramUtils init logger')
  #     print(self.logger)

  # def get_logger(self):
  #     print('InstagramUtils get_logger logger')
  #     print(self.logger)
  #     self.logger.debug('InstagramUtils get_logger logger debug')
  #     return self.logger
    
  def request_data(self, url, access_token):
      payload = {'access_token': access_token}
      if Utils.has_trace_enabled(self):
          self.logger.debug('Url: %s' % url)
      response = requests.get(url, params=payload)
      response_as_json = Utils.response_as_json(self, response)
      return response_as_json 

  def get_date(self, arg):
      try:
        return datetime.strptime(arg, DF).date()
      except:
        return self.get_yesterday()

  def get_yesterday(self):
      return date.today() - timedelta(days = 1)
    
  def get_start_end_str(self, args, delta = 1):
      date_from, date_to = self.get_start_end_dates(args, delta)
      return (datetime.strftime(date_from, DF), datetime.strftime(date_to, DF))
          
  def get_start_end_dates(self, args, delta = 1):
      date_from = None
      date_to = None
      try:
          if (len(args) == 0):
              date_to = date.today()
              date_from = date_to - timedelta(days = delta)
          elif (len(args) >= 2):
              date_from = datetime.strptime(args[0], DF)
              date_to = datetime.strptime(args[1], DF)
          return (date_from, date_to)
      except:
          self.logger.exception("Error obtaining start/end dates")

