import sys, os, requests, copy, logging
import pymysql
import pkg_resources 
from datetime           import time, timedelta, datetime, tzinfo, date
from ig.instagram_utils import InstagramUtils
#from alerts_pb2 import InternalAlert

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
is_imported = None

class HashtagsMediaFetcher:

  SOURCE_DF = "%Y-%m-%dT%H:%M:%S"
  TARGET_DF = "%Y-%m-%d %H:%M:%S"

  ### Build HashtagsMediaFetcher according to how it's being used
  def __init__(self):
    try:
      if is_imported:
        print('HashtagsMediaFetcher as module')
        logger, conf_file = config_fetcher_as_module()
      else:
        print('HashtagsMediaFetcher as main')
        logger, conf_file = config_fetcher_as_main()
      self.logger = logger
      self.utils = InstagramUtils()
      self.utils.init(conf_file, True)
    except:
      self.logger.exception('Error initializing HashtagsMediaFetcher')

      
  ### Process all users from database
  def process_all(self, dates_arr):  
    try:
      exec_start_time = datetime.now()
      date_from, date_to = self.utils.get_start_end_str(dates_arr)
      conn = self.utils.get_conn('ig')
      users = self.get_users(conn)
      for item in users:
        user_id = item[0]
        hashtag = item[1]
        access_token = item[2]
        self.process_hashtags_media(conn, user_id, hashtag, access_token, date_from, date_to)
      conn.close()
    except:
      self.logger.exception('Error executing script')
    finally:
      self.logger.info('Total time: %s' % (datetime.now() - exec_start_time))

    
  def request_hashtag_id(self, user_id, hashtag, access_token):
    host = self.utils.from_config('graph_api.host')
    path = self.utils.from_config('graph_api.request_ht_id_path').format(**locals())
    url = '%s%s'%(host,path)
    payload = {'access_token': access_token}
    if self.utils.has_trace_enabled():
      self.logger.debug('Url: %s' % url)
      self.logger.debug('Payload: %s' % payload)
    response = requests.get('%s%s'%(host,path), params=payload)
    response_as_json = self.utils.response_as_json(response)
    self.logger.debug('Response id: %s' % response_as_json)
    return response_as_json 


  def request_hashtag_media(self, user_id, access_token, hashtag_id, date_from, date_to):
    host = self.utils.from_config('graph_api.host')
    path = self.utils.from_config('graph_api.request_ht_media_path').format(**locals())
    historic = ''
    if (date_from != None and date_to != None): 
      historic = self.utils.from_config('graph_api.historic_suffix').format(**locals())
    url = '%s%s%s'%(host,path,historic)
    payload = {'access_token': access_token}
    if self.utils.has_trace_enabled():
      self.logger.debug('Url: %s' % url)
      self.logger.debug('Payload: %s' % payload)
    response = requests.get(url, params=payload)
    response_as_json = self.utils.response_as_json(response)
    self.logger.debug('Response media: %s' % response_as_json)
    return response_as_json 


  def get_users(self, conn):
    users = list()
    try:
      query = self.utils.from_config("queries.get_users")
      cursor = conn.cursor(pymysql.cursors.SSCursor)
      cursor.execute(query)
      users = list()
      while (1):
        row = cursor.fetchone()
        if not row:
          break
        user_id = row[0].decode('UTF-8')
        hashtag = row[1].decode('UTF-8')
        access_token = row[2].decode('UTF-8')
        users.append((user_id, hashtag, access_token))
        self.logger.debug("Adding user_id %s"%(user_id))
      cursor.close()
      self.logger.debug("Added %s users "%(len(users)))
    except:
      self.logger.exception("Error while getting users")
    return users


  def parse_and_insert(self, conn, user_id, data, hashtag):      
    cursor = conn.cursor()
    cursor.execute('SET character_set_connection=utf8mb4;')
    for item in data:
      media_url = str(item.get("media_url", ""))
      values = {"id" : str(item["id"]),
                "user_id": 0,
                "created_at": str(datetime.utcnow()), # info not present
                "fetched_at": str(datetime.utcnow()),
                "type": str(item.get("media_type",'')),
                "caption": str(item.get("caption",'')).replace("'",'"'),
                "url": str(item.get("permalink",'')),
                "likes_count": item.get("like_count",0),
                "comments_count": item.get("comments_count",0),
                "image": media_url}
      command = self.utils.from_config('queries.insert_media').format(**values)
      if self.utils.has_trace_enabled():
          self.logger.debug("insert command: %s" % command)
      cursor.execute(command)
      conn.commit()

      ht_values = {"media_id": str(item["id"]),
                   "hashtag": hashtag,
                   "lower_hashtag": str.lower(hashtag),
                   "created_at": str(datetime.utcnow())}
      ht_command = self.utils.from_config('queries.insert_ht').format(**ht_values)
      if self.utils.has_trace_enabled():
          self.logger.debug("insert_ht command: %s" % ht_command)
      cursor.execute(ht_command)
      conn.commit()
    self.logger.debug("Inserted %s media for hashtag '%s'" % (len(data), hashtag))
    cursor.close()

  
# def send_alert(alert_text, alert_type, alert_priority):
#   alert = InternalAlert()
#   alert.priority = alert_priority    # {INFO, WARN, SEVERE}
#   alert.type = "IG_FETCH_MEDIA"
#   alert.project = alert_type
#   alert.text = alert_text
#   alert.created_at = int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())*1000
#   body = alert.SerializeToString()
#   url='http://trb-message-exchange-hrd.appspot.com/alert/internal'
#   self.logger.debug('alert url: %s' % url)
#   self.logger.debug('alert body: %s...' % body[:250])
#   r = requests.post(url, body)


  ### Main function
  def process_hashtags_media(self, conn, user_id, hashtag, access_token, date_from_param = None, date_to_param = None):
    try:
      if date_from_param != None and date_to_param != None:
        dates = [date_from_param, date_to_param]
      else:
        dates = []
      date_from, date_to = self.utils.get_start_end_str(dates)
      id_response = self.request_hashtag_id(user_id, hashtag, access_token)
      if id_response and id_response["data"]!=None and len(id_response["data"])>0:
        hashtag_id = id_response["data"][0]["id"]
        response=self.request_hashtag_media(user_id, access_token, hashtag_id,
                                            date_from, date_to)
        self.parse_and_insert(conn, user_id, response.get('data'), hashtag)
    except:
      self.logger.exception("Error while parsing or inserting %s" % hashtag)

      
### If used as main: set Stream+File log handlers and local config file
def config_fetcher_as_main():
  print('Setting Stream+File log handlers and local config file.')

  # configure root logger
  frmttr = self.logger.Formatter(LOG_FORMAT)
  logger = self.logger.getLogger() # root logger 
  logger.setLevel('DEBUG')

  # add console handler
  ch = self.logger.StreamHandler()
  ch.setFormatter(frmttr)
  logger.addHandler(ch)

  # add file handler
  log_file = 'logs/get_topmedia_in_hashtag.log'
  d = os.path.dirname(log_file)
  if not os.path.exists(d) and d != '':
    os.makedirs(d)
  fh = self.logger.FileHandler(log_file)
  fh.setFormatter(frmttr)
  logger.addHandler(fh)

  # configure other loggers
  self.logger.getLogger('urllib3').setLevel('WARNING')
  self.logger.getLogger('shared').setLevel('INFO')

  # initialize Fetcher with local file
  conf_file = "ig/conf/get_topmedia_in_hashtag.yaml"
  return (logger, conf_file)


### If used as module: set Stream log handler and packaged config file
def config_fetcher_as_module():
  print('Setting Stream log handler and packaged config file')

  # configure module logger
  frmttr = logging.Formatter(LOG_FORMAT)
  logger = logging.getLogger(__name__) # module logger
  logger.setLevel('DEBUG')

  # add console handler
  ch = logging.StreamHandler()
  ch.setFormatter(frmttr)
  logger.addHandler(ch)

  # configure other loggers
  logging.getLogger('urllib3').setLevel('WARNING')
  logging.getLogger('shared').setLevel('INFO')

  # initialize Fetcher with packaged file
  resource_package = __name__
  resource_path = '/'.join(('conf', 'get_topmedia_in_hashtag.yaml'))
  conf_file = pkg_resources.resource_filename(resource_package, resource_path)
  return (logger, conf_file)


### Entrypoint

if __name__ == '__main__':
  # Program used as script: run immediately
  fetcher = HashtagsMediaFetcher()
  fetcher.process_all(sys.argv[1:])
else:
  # Program used as import: set flag
  is_imported = True


