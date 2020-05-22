import csv
import subprocess
import os,time
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool as threads_pool

class Downloader(object):
    def __init__(self,cpus,class_desc_file,annotation_file,save_file):
        super(Downloader,self).__init__()
        self.cpus = cpus
        if self.cpus >= multiprocessing.cpu_count():
            self.cpus = multiprocessing.cpu_count()
        print(f"using_cpus/all_gpus:{self.cpus}/{multiprocessing.cpu_count()}")
        self.threads = threads_pool(self.cpus*2)
        try:
            infile = open(class_desc_file, mode='r')
            reader = csv.reader(infile)
            self.dict_list = {rows[1]: rows[0] for rows in reader}
            infile.close()
        except :
            exit()
        #print(self.dict_list.items())
        self.annotation_file = annotation_file
        self.mode = self.annotation_file.split("-")[-3]
        self.save_file = save_file
    def run(self,class_list):
        for cls_id,cls in enumerate(class_list):
            try:
                cmd = f"grep {self.dict_list[cls]} {self.annotation_file}"
                #print(cmd)
                cls_annotations = subprocess.run(cmd.split(),stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()
                #print(f"{cls} : {cls_annotations.__len__()} imgs")
            except:
                print(f"""Warning:there is no class named:"{cls}",you have to check!!! """)
                time.sleep(5.0)
                print(f"going next ....")
                continue

            cls_imgs_file = f"{self.save_file}/JPEGImages/{self.mode}/{cls}"
            cls_labs_file = f"{self.save_file}/Annotations/{self.mode}/{cls}"
            if not os.path.exists(cls_imgs_file):
                os.makedirs(cls_imgs_file)
            if not os.path.exists(cls_labs_file):
                os.makedirs(cls_labs_file)

            '''download the images'''
            cmdds = []
            for id,line in enumerate(cls_annotations):
                '''getting the labels'''
                line_split = line.split(",")
                with open(f"{cls_labs_file}/{line_split[0]}.txt","a") as fp:
                    fp.write(" ".join([str(cls_id),str(float(line_split[4])),str(float(line_split[6])),
                                        str(float(line_split[5])),str(float(line_split[7]))])+"\n")
                cmdd = f"""aws s3 --no-sign --request --only-show-errors cp s3://open-images-dataset/{self.annotation_file.split("-")[-3]}/{line_split[0]}.jpg {cls_imgs_file}/{line_split[0]}.jpg"""
                cmdds.append(cmdd)
                #print(cmdd)
            cmdds = list(set(cmdds))
            print(f"class:{cls},{cmdds.__len__()}images downloading ...")
            list(tqdm(self.threads.imap(os.system, cmdds), total=len(cmdds)))
            self.threads.close()
            self.threads.join()





"""Usage"""

#cpu_counts = 4

'''Officle document of class description and annotation.'''
#cls_file = "class-descriptions-boxable.csv"
#anno_file = "oidv6-train-annotations-bbox.csv"
#anno_file = "validation-annotations-bbox.csv"

'''classes list what you want'''
#geting_class =["Person","Apple"]

'''saving path'''
#save_path = "data"

'''init...'''
#downloader = Downloader(cpu_counts,cls_file,anno_file,save_path)

'''running...'''
#downloader.run(geting_class)