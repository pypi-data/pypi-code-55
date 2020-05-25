import sys, os, requests, logging
import pymysql
import pkg_resources 
from datetime           import time, timedelta, datetime, tzinfo, date
from ig.instagram_utils import InstagramUtils
#from alerts_pb2 import InternalAl

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
is_imported = None

class BusinessMediaFetcher:

  SOURCE_DF = "%Y-%m-%dT%H:%M:%S"
  TARGET_DF = "%Y-%m-%d %H:%M:%S"

  ### Build BusinessMediaFetcher according to how it's being used
  def __init__(self):
    try:
      if is_imported:
        print('BusinessMediaFetcher as module')
        logger, conf_file = config_fetcher_as_module()
      else:
        print('BusinessMediaFetcher as main')
        logger, conf_file = config_fetcher_as_main()
      self.logger = logger
      self.utils = InstagramUtils()
      self.utils.init(conf_file, True)
    except:
      self.logger.exception('Error initializing BusinessMediaFetcher')
      

  ### Utility to build fetching url
  def build_url(self, type, user_id, access_token):
    host = self.utils.from_config('graph_api.host')
    path = self.utils.from_config('graph_api.request_%s_path'%type).format(**locals())
    self.logger.debug('host: %s'%host)
    self.logger.debug('path: %s'%path)
    return '%s%s'%(host,path)

  
  ### Process all users from database
  def process_all(self, arg):
    try:
      exec_start_time = datetime.now()
      date_limit = self.utils.get_date(arg)
      conn = self.utils.get_conn('ig')
      users = self.get_users(conn)
      for item in users:
        user_id = item[0]
        access_token = item[1]
        self.process_business_media(conn,user_id,access_token,date_limit)
      conn.close()
    except:
      self.logger.exception("Error while preparing to process all")
    finally:
      self.logger.info('Total time: %s' % (datetime.now() - exec_start_time))


  ### Get users from database
  def get_users(self, conn):
    users = list()
    try:
      query = self.utils.from_config("queries.get_users")
      cursor = conn.cursor(pymysql.cursors.SSCursor)
      cursor.execute(query)
      while (1):
        row = cursor.fetchone()
        if not row:
          break
        user_id = row[0].decode('UTF-8')
        access_token = row[1].decode('UTF-8')
        users.append((user_id, access_token))
        self.logger.debug("Adding user_id %s"%(user_id))
      cursor.close()
      self.logger.debug("Added %s users "%(len(users)))
    except:
      self.logger.exception("Error while getting users")
    return users


  ### Parse and insert a page of results
  def parse_and_insert(self, conn, user_id, data, is_story=False):
    if len(data) == 0:
      return
    user_values = {"id": user_id, "username": data[0]["username"]}
    command = self.utils.from_config('queries.insert_empty_user').format(**user_values)
    cursor = conn.cursor() 
    cursor.execute(command)
    conn.commit()
    cursor.close()
    
    cursor = conn.cursor()
    cursor.execute('SET character_set_connection=utf8mb4;')
    for item in data:
      created_datetime = datetime.strptime(item["timestamp"][:19], self.SOURCE_DF)
      created_at = datetime.strftime(created_datetime, self.TARGET_DF)
      values = {"id" : str(item["id"]),
                "user_id": str(user_id),
                "created_at": str(created_at),
                "fetched_at": str(datetime.utcnow()),
                "type": str(item.get("media_type",'')),
                "caption": item.get("caption", '').replace("'",'"'),
                "url": str(item.get("permalink", '')),
                "likes_count": item.get("like_count", 0),
                "comments_count": item.get("comments_count", 0),
                "image": str(item.get("media_url", '')),
                "is_story": 1 if is_story else 0}
      min_date = self.utils.get_date(created_at)
      command = self.utils.from_config('queries.insert_media').format(**values)
      if self.utils.has_trace_enabled():
          self.logger.debug("insert_media command: %s" % command)
      cursor.execute(command)
    conn.commit()
    cursor.close()
    return min_date

  
  # IP 189.216.115.149/32
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
  def process_business_media(self, conn, user_id, access_token, date_limit = None):
    try:
        self.logger.info("##############################################")
        self.logger.info("Getting media for %s" % user_id)      
        paginate = True
        url = self.build_url('media',user_id,access_token)
        has_data = False
        while paginate:
          response = self.utils.request_data(url, access_token)
          if response and response.get('data'):
            has_data = True
            data = response.get('data')
            next_url = response.get('paging').get('next')
            self.logger.debug("pagination next_url=%s"%next_url)
            min_date = self.parse_and_insert(conn, user_id, data)
            self.logger.debug("pagination min_date=%s"%min_date)
            if min_date < date_limit or next_url == None:
              self.logger.debug("pagination stopped: min_date=%s"%min_date)
              paginate = False
            url = next_url
          else:
            paginate = False
                  
        self.logger.info("##############################################")
        self.logger.info("Getting stories for %s" % user_id)
        url = self.build_url('stories',user_id,access_token)
        response = self.utils.request_data(url, access_token)
        if response and response.get('data'):
          has_data = True
          self.parse_and_insert(conn, user_id, response.get('data'), True)
        return has_data
    except:
        self.logger.exception("Error while parsing or inserting %s"%user_id)

        
        
### If used as main: set Stream+File log handlers and local config file
def config_fetcher_as_main():
  print('Setting Stream+File log handlers and local config file.')

  # configure root logger
  frmttr = logging.Formatter(LOG_FORMAT)
  logger = logging.getLogger() # root logger 
  logger.setLevel('DEBUG')

  # add console handler
  ch = logging.StreamHandler()
  ch.setFormatter(frmttr)
  logger.addHandler(ch)

  # add file handler
  log_file = 'logs/get_business_media.log'
  d = os.path.dirname(log_file)
  if not os.path.exists(d) and d != '':
    os.makedirs(d)
  fh = logging.FileHandler(log_file)
  fh.setFormatter(frmttr)
  logger.addHandler(fh)

  # configure other loggers
  logging.getLogger('urllib3').setLevel('WARNING')
  logging.getLogger('shared').setLevel('INFO')

  # initialize Fetcher with local file
  conf_file = "ig/conf/get_business_media.yaml"
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
  resource_path = '/'.join(('conf', 'get_business_media.yaml'))
  conf_file = pkg_resources.resource_filename(resource_package, resource_path)
  return (logger, conf_file)


### Entrypoint

if __name__ == '__main__':
  # Program used as script: run immediately
  fetcher = BusinessMediaFetcher()
  fetcher.process_all(sys.argv[1:])
else:
  # Program used as import: set flag
  is_imported = True
  


     
