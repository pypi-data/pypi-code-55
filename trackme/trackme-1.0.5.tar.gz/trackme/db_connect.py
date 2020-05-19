import pymongo
import ssl
import trackme.config

mongo = pymongo.MongoClient(trackme.config.mongoclient, ssl_cert_reqs=ssl.CERT_NONE)
