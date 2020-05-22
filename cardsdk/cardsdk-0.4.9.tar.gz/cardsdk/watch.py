import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class FileEventHandler(LoggingEventHandler):
    def on_moved(self, event):
        logging.info(" - Event :文件/目录： %s 被移动!" % event.src_path)
        # self.cardsdk_build()

    def on_created(self, event):
        logging.info(" - Event :文件/目录： %s 被创建!" % event.src_path)
        # self.cardsdk_build()

    def on_deleted(self, event):
        logging.info(" - Event :文件/目录： %s 被删除!" % event.src_path)
        # self.cardsdk_build()

    def on_modified(self, event):
        logging.info(" - Event :文件/目录： %s 被修改!" % event.src_path)
        self.cardsdk_build()

    def cardsdk_build(self):
        logging.info('cardsdk_build')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()