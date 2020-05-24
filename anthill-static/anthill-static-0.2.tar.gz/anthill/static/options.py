
from anthill.common.options import define

# Main

define("host",
       default="http://localhost:9515",
       help="Public hostname of this service",
       type=str)

define("listen",
       default="port:9515",
       help="Socket to listen. Could be a port number (port:N), or a unix domain socket (unix:PATH)",
       type=str)

define("name",
       default="static",
       help="Service short name. User to discover by discovery service.",
       type=str)

# MySQL database

define("db_host",
       default="127.0.0.1",
       type=str,
       help="MySQL database location")

define("db_username",
       default="root",
       type=str,
       help="MySQL account username")

define("db_password",
       default="",
       type=str,
       help="MySQL account password")

define("db_name",
       default="dev_static",
       type=str,
       help="MySQL database name")

# Rate limit cache

define("rate_cache_host",
       default="127.0.0.1",
       help="Location of a ratelimit cache (redis).",
       group="ratelimit",
       type=str)

define("rate_cache_port",
       default=6379,
       help="Port of ratelimit cache (redis).",
       group="ratelimit",
       type=int)

define("rate_cache_db",
       default=7,
       help="Database of ratelimit cache (redis).",
       group="ratelimit",
       type=int)

define("rate_cache_max_connections",
       default=500,
       help="Maximum connections to the ratelimit cache (connection pool).",
       group="ratelimit",
       type=int)

define("rate_file_upload",
       default="10,600",
       help="A limit for file upload for user tuple: (amount, time)",
       group="ratelimit",
       type=str)

# Static

define("max_file_size",
       default=104857600,
       help="Maximum file size to upload",
       group="static",
       type=int)

# Local storage

define("data_runtime_location",
       default="/usr/local/anthill/static-runtime",
       help="DLC content runtime folder",
       group="static",
       type=str)

define("data_host_location",
       default="http://127.0.0.1:9515/download/",
       help="DLC content prefix URL",
       group="static",
       type=str)