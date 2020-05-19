"""
Config
"""
import logging
secret_key = '5791628bb0b13ce0c676dfde280ba245'
mongoclient = 'mongodb+srv://BohdanVey:newpassword@cluster0-rkq6t.gcp.mongodb' \
              '.net/test?retryWrites=true&w=majority'
mongoname = 'mongologinexample'
NUMBER_WORDS = 20
flask_key = 'newsecretkey'
BOT_TOKEN = "687710974:AAFfjf5i0k4OOrf3m6fauNIq1l4PAB-cTu4"

# GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
# CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

GOOGLE_CHROME_BIN = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
# CHROMEDRIVER_PATH = '/home/bohdan/Downloads/chromedriver'
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'

logger = logging.getLogger("main_logger")