import os

DOCKER_COMPOSE_FILE = """
version: '3'
services:
  redis:
    image: redis:alpine
  meta:
    image: apisgarpun/meta-loc:latest
    depends_on:
      - redis
    ports:
      - "9999:8080"
    volumes:
      - ~/.rwmeta:/root/.rwmeta:delegated
      - {CWD}/meta_conf:/root/meta_conf:delegated
      - {CWD}/:/root/workspace/production:delegated
    environment:
      JAVA_OPTS: -Duser.timezone=Europe/Moscow -Xms1000m -Xmx2500m -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9010 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=localhost
      META_CONFIG: /root/meta_conf/meta-loc-dev.yaml
      RELEASE_VERSION2: dev
      RELEASE_VERSION: local_dev
      META_APP_CONTENT_CONFIG_DIR: /root/meta_conf
      META_APP_CONTENT_WORKSPACE_DIR: /root/workspace
"""


def start_meta():
    cwd = os.getcwd()
    print("cwd = %s" % str(cwd))
