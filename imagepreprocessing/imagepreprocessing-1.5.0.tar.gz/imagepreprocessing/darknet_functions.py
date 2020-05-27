import os
import random
import pickle
import itertools 
from shutil import copyfile


from imagepreprocessing.file_operations import __read_from_file, __write_to_file
from imagepreprocessing.convert_annotations import __convert_annotations_opencv_to_yolo, __convert_annotations_yolo_to_opencv
from imagepreprocessing.other_functions import __run_shell_command
from imagepreprocessing.cfg_templates import __get_cfg_template


# yolo functions

def create_training_data_yolo(source_path, yolo_version=3, percent_to_use = 1, validation_split = 0.2, create_cfg_file=True, train_machine_path_sep = "/", shuffle = True, files_to_exclude = [".DS_Store","train.txt","test.txt","obj.names","obj.data","yolo-obj.cfg","yolo-custom.cfg"]):
    """
    Creates required training files for yolo 

    # Arguments:
        source_path: source path of the images see input format (source folder name of the images will be used to create paths see output format)
        yoo_version: (3) yolo version 3 or 4 
        percent_to_use (1): percentage of data that will be used
        validation_split (0.2): splits validation data with given percentage give 0 if you don't want validation split
        create_cfg_file (True): creates a cfg file with default options for yolov3
        auto_label_by_center (False): creates label txt files for all images labels images by their center automatically (use it if all of your datasets images are centered)
        train_machine_path_sep ("/"): if you are going to use a windows machine for training change this  
        shuffle (True): shuffle the paths
        files_to_exclude ([".DS_Store","train.txt","test.txt","obj.names","obj.data","yolo-obj.cfg","yolo-custom.cfg"]): list of file names to exclude in the image directory (can be hidden files)

    # Save:
        Creates train.txt and test.txt files

    # Input format:
        source_path = some_dir
        
        /some_dir
        ├──/class1
            ├──img1.jpg
            ├──img2.jpg
        ├──/class2
            ├──img3.jpg

    # Output format:
        /some_dir
        train.txt --> data/your_source_folder_name/class1/img1.jpg
        test.txt   
        obj.data
        obj.names                
    """


    # get all file names from main dir and sort the directories
    CATEGORIES = os.listdir(source_path)  
    CATEGORIES.sort()           

    # remove excluded files
    for exclude in files_to_exclude:
        if exclude in CATEGORIES: 
            CATEGORIES.remove(exclude)
    
    source_folder = os.path.basename(source_path)


    # check yolo version
    if(yolo_version == 3):
        train_info = "Download darknet53.conv.74 and move it to darknets root directory.(there are download links on https://github.com/AlexeyAB/darknet)\nAlso move your dataset file to darknet/data/{0}\nRun the command below in the darknets root directory to start training.".format(source_folder)
        train_command1 = "Your train command with map is: ./darknet detector train data/{0}/obj.data data/{0}/yolo-custom.cfg darknet53.conv.74 -map".format(source_folder)
        train_command2 = "Your train command for multi gpu is: ./darknet detector train data/{0}/obj.data data/{0}/yolo-custom.cfg darknet53.conv.74 -gpus 0,1 -map".format(source_folder)
    elif(yolo_version == 4):
        train_info = "Download yolov4.conv.137 and move it to darknets root directory.(there are download links on https://github.com/AlexeyAB/darknet)\nAlso move your dataset file to darknet/data/{0}\nRun the command below in the darknets root directory to start training.".format(source_folder)
        train_command1 = "Your train command with map is: ./darknet detector train data/{0}/obj.data data/{0}/yolo-custom.cfg yolov4.conv.137 -map".format(source_folder)
        train_command2 = "Your train command for multi gpu is: ./darknet detector train data/{0}/obj.data data/{0}/yolo-custom.cfg yolov4.conv.137 -gpus 0,1 -map".format(source_folder)
    else:
        raise ValueError("unsupported yolo version")


    # change path seperator if needed
    save_path = "data/{0}/".format(source_folder).replace("/",train_machine_path_sep)

    # prepare obj.data
    objdata = []
    objdata.append("classes = {0}".format(len(CATEGORIES)))
    objdata.append("train  = data/{0}/train.txt".format(source_folder).replace("/",train_machine_path_sep))
    objdata.append("valid  = data/{0}/test.txt".format(source_folder).replace("/",train_machine_path_sep))
    objdata.append("names = data/{0}/obj.names".format(source_folder).replace("/",train_machine_path_sep))
    objdata.append("backup = backup")


    total_image_count = 0
    image_names = []
    # loop in the main directory
    for category_index, category in enumerate(CATEGORIES):

        path = os.path.join(source_path, category)
        number_of_categories = len(CATEGORIES)
        index_of_category = CATEGORIES.index(category)
        images = os.listdir(path)

        # exclude possible annotation files
        images = list(filter(lambda x: ".txt" not in x, images))

        # fix possible percentage error
        if(percent_to_use <= 0 or percent_to_use > 1):
            raise ValueError("Percentage should be between 0 and 1")
        elif(int(percent_to_use * len(images)) == 0):
            raise ValueError("Percentage is too small for this set")
        else:
            stop_index = int(len(images)*percent_to_use)


        # loop inside each category folder   itertools for stoping on a percentage
        for image_index, img in enumerate(itertools.islice(images , 0, stop_index)):

            # percent info
            print("File name: {} - {}/{}  Image:{}/{}".format(category, index_of_category+1, number_of_categories, image_index+1, stop_index), end="\r")

            # using save_path's last character (data/obj/ or data\\obj\\) to separete inner paths so if operating system is different inner paths will be matches 
            img_and_path = save_path + category + save_path[-1] + img
            image_names.append(img_and_path)
            
            # count images for dividing validation later
            total_image_count += 1
        
        print("")


    # shuffle and divide train and test sets
    if(shuffle):
        random.shuffle(image_names)
    image_names_train = []
    image_names_test = []
    train_percent = int((validation_split * total_image_count))
    image_names_train += image_names[train_percent:]
    image_names_test += image_names[:train_percent]


    # create files
    __write_to_file(image_names_train, file_name = os.path.join(source_path, "train.txt"), write_mode="w")
    __write_to_file(image_names_test, file_name = os.path.join(source_path, "test.txt"), write_mode="w")

    __write_to_file(CATEGORIES, file_name = os.path.join(source_path, "obj.names"), write_mode="w")
    __write_to_file(objdata, file_name = os.path.join(source_path, "obj.data"), write_mode="w")

    print("\n")

    if(create_cfg_file):
        create_cfg_file_yolo(source_path, number_of_categories, yolo_version=yolo_version, batch=64, sub=16, width=416, height=416)

    print("file saved -> {0}\nfile saved -> {1}\nfile saved -> {2}\nfile saved -> {3}\n".format("train.txt", "test.txt","obj.names","obj.data"))
    print(train_info)
    print(train_command1)
    print(train_command2)
    print()


def create_cfg_file_yolo(save_path, classes, yolo_version=3, batch=64, sub=16, width=416, height=416):
    """
    creates config file with default options for yolo3


    # config file structure
    # 0 batch 64
    # 1 sub 8
    # 2 width 416
    # 3 height 416
    # 4 max_batches classes*2000 but no less than 4000
    # 5 steps %80 max_batches
    # 6 steps %90 max_batches
    # 7 classes
    # 8 filters before yolo layers (classes+5)*3
    """
    
    cfg_file_name = "yolo-custom.cfg"

    if(classes < 1):
        raise ValueError("class count can't be smaller than 1") 

    if(width%32 != 0 or height%32 != 0):
        raise ValueError("height and width must be divisible by 32") 

    # get template
    if(yolo_version == 3):
        yolo_cfg_template = __get_cfg_template("yolov3_cfg_template")
    elif(yolo_version == 4):
        yolo_cfg_template = __get_cfg_template("yolov4_cfg_template")
    else:
        raise ValueError("unsupported yolo version") 

    # set up parameters
    if(classes == 1):
        max_batches = 4000
    else:
        max_batches = classes * 2000

    steps1 = int((max_batches * 80) /100)
    steps2 = int((max_batches * 90) /100)

    filters = (classes+5)*3

    yolo_cfg_template = yolo_cfg_template.format(batch,sub,width,height,max_batches,steps1,steps2,classes,filters)

    # save cfg to save path
    __write_to_file([yolo_cfg_template], os.path.join(save_path, cfg_file_name), write_mode="w")

    print("file saved -> {0}".format(cfg_file_name))


def auto_annotation_by_random_points(images_path, class_of_images, annotation_points=((0.5,0.5), (0.5,0.5), (1.0,1.0), (1.0,1.0)), files_to_exclude = [".DS_Store"]):
    """
    # auto creates random annotations for all images (default values labels by center)
    # it needs 4 tuples ((smallest_x, biggest_x), (smallest_y, biggest_y), (smallest_w, biggest_w), (smallest_h, biggest_h))
    # example ((0.4,0.6),(0.4,0.6),(0.8,0.9),(0.8,0.9))
    # values should be between 0 and 1 for yolo to work
    """

    images = os.listdir(images_path)

    # remove excluded files
    for exclude in files_to_exclude:
        if exclude in images: 
            images.remove(exclude)
    
    # exclude possible annotation files
    images = list(filter(lambda x: ".txt" not in x, images))


    # loop inside each category folder   itertools for stoping on a percentage
    for image_index, img in enumerate(images):

        # percent info
        print("Image:{}/{}".format(image_index+1, len(images)), end="\r")

        c1 = random.uniform(annotation_points[0][0], annotation_points[0][1])
        c2 = random.uniform(annotation_points[1][0], annotation_points[1][1])
        
        w = random.uniform(annotation_points[2][0], annotation_points[2][1])
        h = random.uniform(annotation_points[3][0], annotation_points[3][1])
        
        yolo_labels = "{0} {1:7f} {2:7f} {3:7f} {4:7f}".format(class_of_images, c1,c2, w, h)
        
        basename, extension = os.path.splitext(img)
        txtname = basename + ".txt"
        abs_save_path = os.path.join(images_path, txtname)

        __write_to_file([yolo_labels], file_name = abs_save_path, write_mode="w")


def yolo_annotation_tool(images_path, class_names_file, max_windows_size=(1200,700), image_extensions = [".jpg", ".JPG", ".jpeg", ".png", ".PNG"]):
    """
    annotation tool for yolo labeling
    
    # warning it uses two global variables (__coords__, __drawing__) due to the opencvs mouse callback function

    # usage 
    a go backward
    d go forward
    s save selected annotations
    z delete last annotation
    r remove unsaved annotations
    c clear all saved annotations
    """
    import cv2 
    import numpy as np


    # read images
    images = os.listdir(images_path)
    images.sort()

    # remove not included files
    for image in images:
        image_name, image_extension = os.path.splitext(image)
        if image_extension not in image_extensions: 
            images.remove(image)        

    # add paths to images
    images = [os.path.join(images_path, image) for image in images]

    # read class names
    class_names = __read_from_file(class_names_file)
    class_names = class_names.split()


    # -----unused-----
    def __on__trackbar_change(image):
        """
        Callback function for trackbar
        """
        pass
        
    def __resize_with_aspect_ratio(image, width, height, inter=cv2.INTER_AREA):
        """
        resize image while saving aspect ratio
        """
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if h > w:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        image = cv2.resize(image, dim, interpolation=inter)

        return image
    # ---------------



    def __draw_rectangle_on_mouse_drag(event, x, y, flags, param):
        """
        draws rectangle with mouse events
        """
        global __coords__, __drawing__

        if event == cv2.EVENT_LBUTTONDOWN:
            __coords__ = [(x, y)]
            __drawing__ = True
        
        elif event == 0 and __drawing__:
            __coords__[1:] = [(x, y)]
            im = image.copy()
            cv2.rectangle(im, __coords__[0], __coords__[1], (255, 0, 0), 2)
            cv2.imshow(window_name, im) 

        elif event == cv2.EVENT_LBUTTONUP:
            # __coords__.append((x, y))
            __coords__[1:] = [(x, y)]
            __drawing__ = False
    
            cv2.rectangle(image, __coords__[0], __coords__[1], (255, 0, 0), 2)

            # add points
            points.append(((label),__coords__[0],__coords__[1]))


        elif event == cv2.EVENT_RBUTTONDOWN:
            pass

    def __save_annotations_to_file(image_path, yolo_labels_lists, write_mode):
        """
        saves yolo annnotations lists to annotations file list of lists:[[0,1,1,1,1],[1,0,0,0,0]]
        returns annotation_file_path 
        """

        # prepare the annotations
        yolo_labels = []
        for yolo_labels_list in yolo_labels_lists:
            yolo_labels.append("{0} {1:.6} {2:.6} {3:.6} {4:.6}".format(yolo_labels_list[0], yolo_labels_list[1], yolo_labels_list[2], yolo_labels_list[3], yolo_labels_list[4]))

        image_name, image_extension = os.path.splitext(image_path)
        annotation_file_path = "{0}.txt".format(image_name)

        # if last character of the file is not \n we cant append directly we should add another line 
        # since __write_to_file function writes lists to line inserting an empty string automatically creates a new line
        if(os.path.exists(annotation_file_path)):
            temp_file_content = __read_from_file(annotation_file_path)
            if(temp_file_content):
                if(temp_file_content[-1][-1] != "\n"):
                    yolo_labels.insert(0,"")

        # write prepared annotations to file
        __write_to_file(yolo_labels, annotation_file_path, write_mode=write_mode)

        return annotation_file_path

    def __load_annotations_from_file(image_path):
        """
        loads an images annotations with using that images path returns none if annotation is not exists
        """
        # checking if the annotation file exists if exists read it
        image_name, image_extension = os.path.splitext(image_path)
        annotation_file_path = "{0}.txt".format(image_name)
        if os.path.exists(annotation_file_path):
            annotations = __read_from_file(annotation_file_path)
            annotations = annotations.split("\n")
            annotations = filter(None, annotations)  # delete empty lists 
            annotations = [annotation.split() for annotation in annotations]
            # convert annotations to float and label to int
            # yolo annotation structure: (0 0.8 0.8 0.5 0.5)
            for annotation in annotations:
                annotation[0] = int(annotation[0])
                annotation[1] = float(annotation[1])
                annotation[2] = float(annotation[2])
                annotation[3] = float(annotation[3])
                annotation[4] = float(annotation[4])
            return annotations
        else:
            return None

    def __draw_bounding_boxes_to_image(image_path, class_names):
        """
        draw annotations if file is exists
        """

        # loading annotation file if exists
        annotations = __load_annotations_from_file(image_path)

        if(not annotations):
            return None, 0

        # loading image 
        image = cv2.imread(image_path)
        
        # get dimensions of image
        image_height = np.size(image, 0)
        image_width = np.size(image, 1)

        # convert points
        opencv_points = __convert_annotations_yolo_to_opencv(image_width, image_height, annotations)

        # draw the rectangles using converted points
        for opencv_point in opencv_points:
            # give error if an annoted file has impossible class value
            if(opencv_point[0] > len(class_names)-1):
                raise ValueError("this txt file has an annotation that has bigger class number than current selected class file") 

            cv2.rectangle(image, (opencv_point[1], opencv_point[2]), (opencv_point[3], opencv_point[4]), (0,200,100), 2)
            cv2.line(image, (opencv_point[1], opencv_point[2]), (opencv_point[3], opencv_point[4]), (255, 0, 0), 1) 
            cv2.putText(image, "{0}".format(class_names[opencv_point[0]]), (opencv_point[1], opencv_point[2]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color=(0, 0, 0), thickness=2)

        return image, len(annotations)

    def __refresh_image(image_index, label):
        """
        if annotation file exists draw the rectangles resize and return the image if not just return the resized image
        also draw information to the image
        """
        image, annoted_object_count = __draw_bounding_boxes_to_image(images[image_index], class_names)
        if(image is None):
            image = cv2.imread(images[image_index])
        # image = __resize_with_aspect_ratio(image, max_windows_size[0], max_windows_size[1])
        image = cv2.resize(image, max_windows_size)

        if(annoted_object_count == 0):
            __save_annotations_to_file(images[image_index], [], "w")
        
        # show some info with puttext
        cv2.putText(image, "{0}/{1} objects:{2} label: {3}".format(len(images), image_index+1, annoted_object_count, class_names[label]), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color=(0, 200, 100), thickness=2)

        return image 


    

    points = []
    image_index = 0
    label_temp = 0
    global __drawing__
    __drawing__ = False
    window_name = "Yolo annotation tool"


    # create window and set it up
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, 40,30)
    cv2.setMouseCallback(window_name, __draw_rectangle_on_mouse_drag,image)
    cv2.createTrackbar('label', window_name, 0, len(class_names)-1, __on__trackbar_change)
    image = __refresh_image(image_index, 0)

    # gui loop
    while(True):

        label = cv2.getTrackbarPos('label', window_name)
        
        # bu ne salak yontem lan kafan mi iyidi yaparken
        if(label != label_temp):
            image = __refresh_image(image_index, label)
            label_temp = label
            points = []

        # dont refresh the original frame while drawing
        if(not __drawing__):
            cv2.imshow(window_name, image)  
        
        key = cv2.waitKey(30)
        


        # save selected annotations to a file
        if(key == ord("s")):
            if(len(points) > 0):

                image_height = np.size(image, 0)
                image_width = np.size(image, 1)

                # convert and save annotations to file
                yolo_labels_lists = __convert_annotations_opencv_to_yolo(image_width,image_height,points)
                __save_annotations_to_file(images[image_index], yolo_labels_lists, "a")

                # reset points and refresh image
                image = __refresh_image(image_index, label)
                points = []

                print("annotation saved {0}".format(yolo_labels_lists))



        # move backward
        if(key == ord("a")):
            if(image_index > 0):
                image_index -= 1
                image = __refresh_image(image_index, label)
                points = []

        # move forward
        if(key == ord("d")):
            if(image_index < len(images)-1):
                image_index += 1
                image = __refresh_image(image_index, label)
                points = []

        # delete last annotation
        if(key == ord("z")):
            # load annotations
            yolo_labels_lists = __load_annotations_from_file(images[image_index])            
            if(yolo_labels_lists):
                # delete last one
                yolo_labels_lists.pop()
                # save new annotations (last one deleted)
                annotation_file_path = __save_annotations_to_file(images[image_index], yolo_labels_lists, "w")
                image =__refresh_image(image_index, label)
                points = []

                # # if file is empty delete it
                # if(len(yolo_labels_lists) == 0):
                #     os.remove(annotation_file_path)

        # refresh current image
        if(key == ord("r")):
            image =__refresh_image(image_index, label)
            points = []

        # clear annotations
        if(key == ord("c")):
            __save_annotations_to_file(images[image_index], [], "w")
            image = __refresh_image(image_index, label)        
            points = []


        # if window is closed break this has to be after waitkey
        if (cv2.getWindowProperty(window_name, 0) < 0):
            # cv2.destroyAllWindows()
            break

        # quit on esc
        if(key == 27):
            break


    cv2.destroyAllWindows()


def make_prediction_from_directory_yolo(images_path, darknet_path, save_path = "detection_results", darknet_command = "./darknet detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights {0} -i 0 -thresh 0.2 -dont_show", files_to_exclude = [".DS_Store",""]):
    """
    makes prediction for multiple images from directory
    it uses shell command to execute darknet
    """

    save_path = os.path.join(darknet_path, save_path)

    # make the dir
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    images = os.listdir(images_path)
    images.sort()

    # remove excluded files
    for exclude in files_to_exclude:
        if exclude in images: 
            images.remove(exclude)

    image_count = len(images)
    for index, image in enumerate(images):
        abs_path = os.path.join(images_path, image)
        __run_shell_command("cd {0} && {1}".format(darknet_path,darknet_command.format(abs_path)))
        copyfile(os.path.join(darknet_path, "predictions.jpg"), os.path.join(save_path, "predictions{0}.jpg".format(index)))
        
        print("File name: {0} - {1}/{2}".format(image, index+1, image_count), end="\r")

    print("\nAll images saved to {0}".format(save_path))


def draw_bounding_boxes(images_path_file, class_names_file, save_path = "annoted_images"):
    """
    Draws bounding boxes of images

    # input
    images_path_file: a file that consists of image paths
    class_names_file: class names for bounding boxes
    save_path:("annoted_images") save path of the new images
    """
    import cv2
    import numpy as np

    image_paths = __read_from_file(images_path_file)
    image_paths = image_paths.split()
    
    class_names = __read_from_file(class_names_file)
    class_names = class_names.split()
    
    # make the dir
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for image_path in image_paths:

        image = cv2.imread(image_path)

        # set up save loaction and get annotation file
        image_name, image_extension = os.path.splitext(image_path)
        new_file_name = "{0}(objects){1}".format(image_name, image_extension)
        new_file_save_path = os.path.join(save_path, os.path.basename(new_file_name))
        annotation_file_path = "{0}.txt".format(image_name)

        # parse annotation file
        
        if os.path.exists(annotation_file_path):
            annotations = __read_from_file(annotation_file_path)
            annotations = annotations.split("\n")
            annotations = filter(None, annotations)  # delete empty lists 
            annotations = [annotation.split() for annotation in annotations]
            # convert annotations to float and label to int
            # yolo annotation structure: (0 0.8 0.8 0.5 0.5)
            for annotation in annotations:
                annotation[0] = int(annotation[0])
                annotation[1] = float(annotation[1])
                annotation[2] = float(annotation[2])
                annotation[3] = float(annotation[3])
                annotation[4] = float(annotation[4])
        else:
            continue
            
         # get dimensions of image
        image_height = np.size(image, 0)
        image_width = np.size(image, 1)

        # convert points
        opencv_points = __convert_annotations_yolo_to_opencv(image_width, image_height, annotations)

        # draw the rectangles using converted points
        for opencv_point in opencv_points:
            # give error if an annoted file has impossible class value
            if(opencv_point[0] > len(class_names)-1):
                raise ValueError("this image file has an annotation that has bigger class number than current selected class file") 

            cv2.rectangle(image, (opencv_point[1], opencv_point[2]), (opencv_point[3], opencv_point[4]), (0,200,100), 2)
            cv2.line(image, (opencv_point[1], opencv_point[2]), (opencv_point[3], opencv_point[4]), (255, 0, 0), 1) 
            cv2.putText(image, "{0}".format(class_names[opencv_point[0]]), (opencv_point[1], opencv_point[2]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color=(0, 0, 0), thickness=2)
            
        
        cv2.imwrite(new_file_save_path, image)
        
        print("Image saved: {0}".format(new_file_save_path))












# deprecated
def __create_training_data_yolo(source_path, save_path = "data/obj/", percent_to_use = 1, validation_split = 0.2, rename_duplicates = False, shuffle = True, files_to_exclude = [".DS_Store","data","train.txt","test.txt","obj.names","obj.data"]):
    """
    Creates train ready data for yolo, labels all the images by center automatically
    (This is not the optimal way of labeling but if you need a lot of data fast this is an option)

    # Arguments:
        source_path: source path of the images see input format
        save_path (data/obj/): this path will be added at the begining of every image name in the train.txt and test.txt files
        percent_to_use (1): percentage of data that will be used
        validation_split (0.2): splits validation data with given percentage give 0 if you don't want validation split
        rename_duplicates (False): renames duplicates while copying images but it slows down the process if you don't have any duplicates in your set don't use it
        shuffle (True): shuffle the paths
        files_to_exclude ([".DS_Store","data,"train.txt","test.txt","obj.names","obj.data"]): list of file names to exclude in the image directory (can be hidden files)

    # Save:
        Copies all images in to save_path directory and creates txt files for each image see output format

    # Input format:
        (if there are duplicates you can use rename duplicates)
        source_path = some_dir
        
        /some_dir
        ├──/class1
            ├──img1.jpg
            ├──img2.jpg
            ├──img3.jpg
        ├──/class2
            ├──img3.jpg

    # Output format:
        (if rename duplicates is on it renames images)
        source_path = some_dir
        save_path = "data/obj/"
        
        /some_dir
        train.txt
        test.txt
        ├──data/obj/
            ├──img1.jpg
            ├──img1.txt
            ├──img2.jpg
            ├──img2.txt
            ├──img3.jpg
            ├──img3.txt
            ├──img3(1).jpg
            ├──img3(1).txt                  
    """

    image_names = [] 
    
    CATEGORIES = os.listdir(source_path)  # get all file names from main dir
    CATEGORIES.sort()                     # sort the directories

    # remove excluded files
    for exclude in files_to_exclude:
        if exclude in CATEGORIES: 
            CATEGORIES.remove(exclude)
    
    # make the dir
    if not os.path.exists(os.path.join(source_path, save_path)):
        os.makedirs(os.path.join(source_path, save_path))
    
    total_image_count = 0

    # loop in the main directory
    for category_index, category in enumerate(CATEGORIES):


        path = os.path.join(source_path, category)
        number_of_categories = len(CATEGORIES)
        index_of_category = CATEGORIES.index(category)
        images = os.listdir(path)

        # fix possible percentage error
        if(percent_to_use <= 0 or percent_to_use > 1):
            print("Enter a possible percentage between 0 and 1")
            return
        elif(int(percent_to_use * len(images)) == 0):
            print("Percentage is too small for this set")
            return
        else:
            stop_index = int(len(images)*percent_to_use)

              

        # loop inside each category folder   itertools for stoping on a percentage
        for image_index, img in enumerate(itertools.islice(images , 0, stop_index)):

            # percent info
            print("File name: {} - {}/{}  Image:{}/{}".format(category, index_of_category+1, number_of_categories, image_index+1, stop_index), end="\r")

        
            # yolo label format
            # <object-class> <x_center> <y_center> <width> <height>
            # class 0.5 0.5 1 1 

            yolo_labels = "{0} {1} {2} {3} {4}".format(category_index, 0.5, 0.5, 1, 1)
            
            absolute_save_path = os.path.join(source_path, save_path)
            img_and_path = save_path + img

            # if rename duplicates enabled name can be changed but original name is needed to copy the file 
            img_new_name = img

            # rename duplicates if enabled
            if(rename_duplicates):
                duplicate_number = 1
                while(True):
                    if(img_and_path in image_names):

                        # reset the image name tor prevet something like this img(1)(2).jpg
                        img_and_path = save_path + img 

                        # change the image name in the train or test file
                        basename, extension = os.path.splitext(img_and_path)
                        img_and_path = "{0}{1}{2}{3}{4}".format(basename, "(", duplicate_number, ")", extension)
                        
                        # change real image name
                        basename, extension = os.path.splitext(img)
                        img_new_name = "{0}{1}{2}{3}{4}".format(basename, "(", duplicate_number, ")", extension)
                        duplicate_number += 1
                    else:
                        break
            

            basename, _ = os.path.splitext(img_new_name)
            text_name = basename + ".txt"
            path_for_txt_file = os.path.join(absolute_save_path, text_name)
 
            __write_to_file([yolo_labels], path_for_txt_file, write_mode="w")


            # copy_files_to_new_path
            new_path_img = os.path.join(absolute_save_path, img_new_name)            
            copyfile(os.path.join(path, img), new_path_img)

            image_names.append(img_and_path)

            # count images for dividing validation later
            total_image_count += 1
        
        print("")

    # shuffle and divide train and test sets
    if(shuffle):
        random.shuffle(image_names)
    image_names_train = []
    image_names_test = []

    train_percent = int((validation_split * total_image_count))
    image_names_train += image_names[train_percent:]
    image_names_test += image_names[:train_percent]

    # prepare obj.data
    objdata = []
    objdata.append("classes = {0}".format(len(CATEGORIES)))
    objdata.append("train  = data/train.txt")
    objdata.append("valid  = data/test.txt")
    objdata.append("names = data/obj.names")
    objdata.append("backup = backup")

    # save to file
    __write_to_file(image_names_train, file_name = os.path.join(source_path, "train.txt"), write_mode="w")
    __write_to_file(image_names_test, file_name = os.path.join(source_path, "test.txt"), write_mode="w")

    __write_to_file(CATEGORIES, file_name = os.path.join(source_path, "obj.names"), write_mode="w")
    __write_to_file(objdata, file_name = os.path.join(source_path, "obj.data"), write_mode="w")

    print("\nfile saved -> {0}\nfile saved -> {1}\nfile saved -> {2}\nfile saved -> {3}".format("train.txt", "test.txt","obj.names","obj.data"))
