import queue
import multiprocessing
import cryolo.imagereader as imagereader

class BaseFeatureExtractor:

    def __init__(self, images,procs=3):
        self.images = images
        self.procs = procs
        self.num_img_read = 0
        self.queue_size = 15
        self.queue = queue.Queue(maxsize=self.queue_size)

    def done(self):
        return (len(self.images)-self.num_img_read) == 0

    def get_next_image(self):


    def start(self):
        pool = multiprocessing.Pool(processes=self.procs)
        pool.map(imagereader.image_read())


        pass



