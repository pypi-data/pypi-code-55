#!/usr/bin/env python
# coding: utf-8

# In[1]:


try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        from IPython.display import display, Javascript
        display(Javascript('Jupyter.notebook.kernel.execute("nb_name = \'" + Jupyter.notebook.notebook_name + "\'");'));
except:
        pass


# In[100]:


version = '0.59'

import re
import tempfile
import os
import subprocess
import glob
from collections import OrderedDict
import base64
import shutil
import time
import os
import stat
import pickle


# # Helper Functions

# In[101]:


def is_testing():
    try:
        return nb_name == 'lx.ipynb'
    except:
        return False


# In[102]:


def isnotebook():
    try:
        return get_ipython().__class__.__name__ == 'ZMQInteractiveShell'
    except:
        pass
    return False


# In[103]:


def testPrint(*args):
    if is_testing():
        print(*args)


# # Requiremtns

# In[104]:


requirements = []

requirements.append('numpy')
import numpy as np

requirements.append('pandas')
import pandas as pd

requirements.append('natsort')
import natsort

requirements.append('opencv-python')
import cv2

requirements.append('Pillow')
from PIL import Image

requirements.append('urllib3')
from urllib.request import urlopen

requirements.append('ipython')
from IPython.core.display import display, HTML


# # Strings

# In[105]:


def sFloat0(f): return "{:0.0f}".format(f)
def sFloat1(f): return "{:0.1f}".format(f)
def sFloat2(f): return "{:0.2f}".format(f)
def sFloat3(f): return "{:0.3f}".format(f)
def sFloat4(f): return "{:0.4f}".format(f)
def sFloat5(f): return "{:0.5f}".format(f)
def sFloatSci0(f): return "{:0.0E}".format(f)
def sFloatSci1(f): return "{:0.1E}".format(f)
def sFloatSci2(f): return "{:0.2E}".format(f)
def sFloatSci3(f): return "{:0.3E}".format(f)
def sFloatSci4(f): return "{:0.4E}".format(f)
def sFloatSci5(f): return "{:0.5E}".format(f)

if is_testing():
    print(sFloat0(1.234567))
    print(sFloat1(1.234567))
    print(sFloat2(1.234567))
    print(sFloat3(1.234567))
    print(sFloat4(1.234567))
    print(sFloatSci0(1.234567))
    print(sFloatSci1(1.234567))
    print(sFloatSci2(1.234567))
    print(sFloatSci3(1.234567))
    print(sFloatSci4(1.234567))
    print(sFloatSci5(1.234567))


# # Process / Thread

# In[359]:


def mapThread(func, args, n=8):
    from multiprocessing.pool import ThreadPool
    tPool = ThreadPool(n)
    res = tPool.map(func, args)
    return res

def mapProcess(func, args, n=8):
    from multiprocessing import Pool
    pPool = Pool(n)
    res = pPool.map(func, args)
    return res

if is_testing():
    print(mapProcess(str, range(10)))
    print(mapThread(str, range(10)))
    print(list(map(str, range(10))))


# # Lists

# In[314]:


def liChunks(l, chunk_size):
    return [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]


# In[315]:


if is_testing():
    print(liChunks(['a', 'b', 'c', 'd', 'e', 'f'], 1))
    print(liChunks(['a', 'b', 'c', 'd', 'e', 'f'], 2))
    print(liChunks(['a', 'b', 'c', 'd', 'e', 'f'], 3))


# In[308]:


def liSplit(a, number_of_splits):
    idxs = [int(np.round(idx)) for idx in np.linspace(0, len(a), num=number_of_splits + 1)]
    return [a[start:end] for start, end in zip(idxs[:-1], idxs[1:])]


# In[309]:


if is_testing():
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 1))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 2))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 3))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 4))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 5))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 6))


# In[287]:


def liJoin(l):
    out = []
    for e in l:
        out += e
    return out


# In[289]:


if is_testing():
    print(liJoin([['a', 'b', 'c'], ['d', 'e', 'f']]))


# In[355]:


def liFlatten(l):
    if isinstance(l, list) or isinstance(l, tuple):
        out = []
        for e in l:
            flat = liFlatten(e)
            if isinstance(flat, list) or isinstance(flat, tuple):
                out += flat
            else:
                out.append(flat)
        return out
    else:
        return l


# In[358]:


if is_testing():
    print(liFlatten(['aa', ['bb', 'cc'], [['dd', ['ee', 'ff']]]]))
    print(liFlatten([1, ['bb', 3], [['dd', ['ee', 'ff']]]]))


# # List of Strings

# In[110]:


regex_cache = {}
def sListFilter(l, re_include=".*", re_exclude='^\b$'):
    regex_cache[re_include] = regex_cache.get(re_include, re.compile(re_include))
    regex_cache[re_exclude] = regex_cache.get(re_exclude, re.compile(re_exclude))
    return [e for e in l if regex_cache[re_include].search(e) and not regex_cache[re_exclude].search(e)]


# In[111]:


if is_testing():
    sListFilter(['good x', 'other good x', 'without the letter before y'])


# In[112]:


if is_testing():
    print(sListFilter(['good x', 'other good x', 'without the letter before y'], re_include='x'))


# In[113]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+'))


# In[114]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+', re_exclude='z'))


# In[115]:


def lCsv(l, force_oneline=False):
    
    if len(l) == 0:
        return ""
    
    if all([isinstance(e, (list, tuple)) for e in l]) and not force_oneline:
        length = len(l[0])
        if all([len(e) == length for e in l]):
            return "\n".join([lCsv(e, force_oneline=True) for e in l])
            
    return ", ".join([str(e) for e in l])


# In[116]:


if is_testing():
    print(lCsv(['a', 'b', 1, 3.14]))


# In[117]:


if is_testing():
    print(lCsv([['a', 'b'], 1, 3.14]))


# In[118]:


if is_testing():
    print(lCsv([['a', 'b', 1, 3.14], ['c', 'd', 2, 2.72]]))


# # Text files

# In[119]:


def txtread(path):
    if 'http://' in path or 'https://' in path:
        return urlopen(path).read().decode()
    elif 'gs://' in path:
        return gsTxtread(path)
    else:
        with open(path, 'r') as f:
            return f.read()

def txtwrite(path, txt):
    if 'gs://' in path:
        gsTxtwrite(path, txt)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            return f.write(txt)


# In[120]:


if is_testing():
    print(txtread('https://arxiv.org'))


# # List of Strings

# In[121]:


regex_cache = {}
def sListFilter(listOfStrings, re_include=".*", re_exclude='^\b$'):
    regex_cache[re_include] = regex_cache.get(re_include, re.compile(re_include))
    regex_cache[re_exclude] = regex_cache.get(re_exclude, re.compile(re_exclude))
    return [e for e in listOfStrings if regex_cache[re_include].search(e) and not regex_cache[re_exclude].search(e)]


# ### Examples

# In[122]:


if is_testing():
    print(sListFilter(['good x', 'other good x', 'without the letter before y']))


# In[123]:


if is_testing():
    print(sListFilter(['good x', 'other good x', 'without the letter before y'], re_include='x'))


# In[124]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+'))


# In[125]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+', re_exclude='z'))


# In[126]:


if is_testing():
    print(txtread('https://arxiv.org'))


# # GCP Google Cloud Platform

# In[226]:


import warnings
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials from Google Cloud SDK")

def _gsPathSplit(path):
    bucket = path.split("//")[1].split("/")[0]
    prefix = "/".join(path.split("//")[1].split("/")[1:])
    return bucket, prefix

def _gsClient():
    from google.cloud import storage
    client = storage.Client()
    
def _gsBlob(path):
    from google.cloud import storage
    bucket_name, prefix = _gsPathSplit(path)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(prefix)
    return blob


# In[128]:


def gsGsToHttp(path):
    return path.replace("gs://", "https://storage.cloud.google.com/")

def gsHttpToGs(path):
    return path.replace("https://storage.cloud.google.com/", "gs://").split("?")[0] # "?" is for possible "?authuser=0"


# In[375]:


def gsLs(path):
    from google.cloud import storage
    bucket, prefix = _gsPathSplit(path)
    client = storage.Client().bucket(bucket)
    return ['gs://' + bucket + '/' + blob.name for blob in client.list_blobs(prefix=prefix)]


# In[377]:


def gsExists(path):
    from google.cloud import storage
    bucket, prefix = _gsPathSplit(path)
    client = storage.Client().bucket(bucket)
    return client.blob(prefix).exists()


# In[130]:


def gsUploadFile(gsPath, path):
    blob = _gsBlob(gsPath)
    blob.upload_from_filename(path)


# In[131]:


def gsTxtread(path):
    from google.cloud import storage
    bucket_name, source_blob_name = _gsPathSplit(path)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_string().decode()


# In[132]:


def gsTxtwrite(path, s):
    blob = _gsBlob(path)
    return blob.upload_from_string(s)


# In[133]:


def gsImwrite(path, img):
    blob = _gsBlob(path)
    _, encimg = cv2.imencode('.png', img[:, :, [2, 1, 0]])
    blob.upload_from_string(encimg.tobytes())


# In[134]:


def gsImread(path):
    blob = _gsBlob(path)
    raw = np.asarray(bytearray(blob.download_as_string()), dtype="uint8")
    return cv2.imdecode(raw, 1)[:, :, [2, 1, 0]]


# In[135]:


def gsPklWrite(path, obj):
    blob = _gsBlob(path)
    return blob.upload_from_string(pickle.dumps(obj, protocol=4))


# In[136]:


def gsPklRead(path):
    blob = _gsBlob(path)
    return pickle.loads(blob.download_as_string())


# # Pickle

# In[137]:


def pklwrite(path, obj):
    if 'gs://' in path:
        return gsPklWrite(path, obj)
    else:
        with open(path, 'wb') as f:
            return pickle.dump(obj, f, protocol=4)


# In[138]:


def pklread(path):
    if 'gs://' in path:
        return gsPklRead(path)
    else:
        with open(path, 'rb') as f:
            return pickle.load(f)


# In[139]:


if is_testing():
    with tempfile.TemporaryDirectory() as dir_path:
        pkl_path = os.path.join(dir_path, 'test.pkl')
        
        pklwrite(pkl_path, 'test')
        print(pklread(pkl_path))


# # Images

# In[140]:


def imread(path):
    if isinstance(path, np.ndarray) and path.dtype == np.uint8:
        return path
    elif 'http://' in path or 'https://' in path:
        raw = np.asarray(bytearray(urlopen(path).read()), dtype="uint8")
        img = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    elif 'gs://' in path:
        return gsImread(path)
    elif os.path.isfile(path):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img[:, :, [2, 1, 0]] # This converts the cv2 colors to RGB

def imsread(paths):
    if isinstance(paths, str) and os.path.isdir(paths):
        return [imread(path) for path in fiFindByWildcard(os.path.join(paths, "*.png"))]
    assert isinstance(paths, list) or isinstance(paths, tuple), type(paths)
    return [imread(path) for path in paths]

def imwrite(path, img):
    if "gs://" in path:
        gsImwrite(path, img)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, img[:, :, [2, 1, 0]])
    
def imjoin(imgs, axis=1):
    return np.concatenate(imgs, axis=axis)

def impad(img, top=0, bottom=0, left=0, right=0, color=255):
    return np.pad(img, [(top, bottom), (left, right), (0, 0)], 'constant', constant_values=color)


# In[141]:


def imshow(array, scale=1):
    array = imread(array)
    if scale > 1:
        array = imscaleNN(array, scale)
        
    if isnotebook():
        display(Image.fromarray(array))
    else:
        cv2.imshow('img', array[:, :, [2, 1, 0]])
        cv2.waitKey()


# In[142]:


if is_testing():
    img = imread('http://via.placeholder.com/70.png')
    imshow(img)


# In[143]:


if is_testing():
    imshow('http://via.placeholder.com/70.png')


# In[144]:


def imscaleNN(img, s):
    return cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)

def imscaleBic(img, s):
    return cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)


# In[145]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        img = (255 * np.random.rand(20, 20, 3)).astype(np.uint8)
        img_path = os.path.join(d, 'test.png')
        imwrite(img_path, img)
        img_read = imread(img_path)
        
        out = imjoin([impad(img, right=5), img_read]) # join Images side by side

        out_large_pixaleted = imscaleNN(out, 8)
        imshow(out_large_pixaleted)

        out_large_interbic = imscaleBic(out, 8)
        imshow(out_large_interbic)


# In[146]:


def imRepeat(img, height, width):
    height_old, width_old, _ = img.shape

    _ceil = lambda x: int(np.ceil(x))

    img = np.concatenate([img]*_ceil(height/height_old), axis=0)[:height]
    img = np.concatenate([img]*_ceil(width/width_old), axis=1)[:, :width]
    
    return img


# In[147]:


if is_testing():
    img_random_color_3x5 = (np.random.rand(3, 5, 3)*255).astype(np.uint8)
    imshow(imRepeat(img_random_color_3x5, 7, 11), scale=10)


# In[148]:


def imNewWhite(height, width):
    return np.ones((height, width, 3)).astype(np.uint8) * 255


# In[149]:


if is_testing(): imshow(imNewWhite(10, 500) - 30)


# In[150]:


def imNewBlack(height, width):
    return np.zeros((height, width, 3)).astype(np.uint8)


# In[151]:


if is_testing(): imshow(imNewBlack(10, 500))


# In[152]:


def imAddNoiseGauss(img, std):
    assert img.dtype == np.uint8, img.dtype
    noise = np.random.randn(*img.shape) * std
    noisy = (np.clip(img.astype(np.float) + noise.astype(np.float), 0, 255)).astype(np.uint8)
    return noisy

if is_testing(): imshow(imAddNoiseGauss(imread('http://via.placeholder.com/150.png'), 10))


# In[153]:


def imJpgDegradation(img, quality):
    assert img.dtype == np.uint8, img.dtype
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode('.jpg', img, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    return decimg

if is_testing(): imshow(imJpgDegradation(imread('http://via.placeholder.com/150.png'), 15))


# In[154]:


def imCropCenter(img, size):
    h, w, c = img.shape

    h_start = max(h // 2 - size // 2, 0)
    h_end = min(h_start + size, h)

    w_start = max(w // 2 - size // 2, 0)
    w_end = min(w_start + size, w)

    return img[h_start:h_end, w_start:w_end]


# In[155]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 10))


# In[156]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 49))


# In[157]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 50))


# In[158]:


if is_testing(): 
    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 100))


# In[159]:


def imGallery(imgs, pad=0):
    imgs = [imread(img) for img in imgs] # load if path or url
    n = len(imgs)
    nw = int(np.ceil(np.sqrt(n)))
    nh = int(np.ceil(n / nw))
    img_h, img_w, _ = imgs[0].shape
    w = nw * img_w + (nw - 1) * pad
    h = nh * img_h + (nh - 1) * pad

    assert imgs[0].dtype == np.uint8
    assert all([img.shape[0] == img_h for img in imgs])
    assert all([img.shape[1] == img_w for img in imgs])
    out = np.ones((h, w, 3), dtype=np.uint8) * 255

    idx = 0
    for ih in range(nh):
        for iw in range(nw):
            if idx + 1 > len(imgs):
                break
            w_beg = (iw + 0) * (img_w + pad)
            w_end = (iw + 1) * (img_w + pad) - pad
            h_beg = (ih + 0) * (img_h + pad)
            h_end = (ih + 1) * (img_h + pad) - pad
            out[h_beg:h_end, w_beg:w_end] = imgs[idx]
            idx += 1
    return out


# In[160]:


if is_testing():
    # List of images from back to white
    listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]


# In[161]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:1]))


# In[162]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:2]))


# In[163]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:2], pad=1))


# In[164]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:5], pad=1))


# In[165]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:9], pad=1))


# In[166]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:10], pad=1))


# In[167]:


if is_testing():
    img40x20 = imread('http://via.placeholder.com/40x20.png')
    imshow(imGallery([img40x20, img40x20, img40x20], pad=1))


# # Files

# In[168]:


def fiFindByWildcard(wildcard):
    return natsort.natsorted(glob.glob(wildcard, recursive=True))


# In[169]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]
        
        out_dir = os.path.join(d, "sub_dir")
        
        imgs_write = []
        for i in range(10):
            img = imNewBlack(10, 10) + 25 * i
            imwrite(os.path.join(out_dir, "{}.png".format(i)), img)
            imgs_write.append(img)
        
        print("written images:")
        imshow(imGallery(imgs_write))
        
        print("found images:")
        img_paths = fiFindByWildcard(os.path.join(out_dir, "*"))
        imgs = imsread(img_paths)
        imshow(imGallery(imgs))
        
        print("found images:")
        img_paths = fiFindByWildcard(os.path.join(d, "**/*.png"))
        imgs = imsread(img_paths)
        imshow(imGallery(imgs))


# In[170]:


def fiRemove(path):
    os.remove(path)

def fiRemoveDir(path):
    shutil.rmtree(path)

def fiIsEmptyDir(path):
    return len(os.listdir(path)) == 0

def fiSize(path):
    return os.path.getsize(path)

def fiSizeMb(path):
    return os.path.getsize(path) / 2**20

def fiAgeSeconds(path):
    return time.time() - os.stat(path)[stat.ST_MTIME]

def fiAgeMinutes(path):
    return (time.time() - os.stat(path)[stat.ST_MTIME]) / 60

def fiAgeHours(path):
    return (time.time() - os.stat(path)[stat.ST_MTIME]) / 3600


# In[171]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]
        
        out_dir = os.path.join(d, "sub_dir")
        
        imgs_write = []
        img = imNewBlack(100, 100)
        img_path = os.path.join(out_dir, "1.png")
        imwrite(img_path, img)
        
        if not fiIsEmptyDir(out_dir):
            print("out_dir not empty\n")
        print("\n".join(fiFindByWildcard(os.path.join(d, "**", "*"))))
        print("size: " + str(fiSizeMb(img_path)) + " MB")
        print("age: " + str(fiAgeSeconds(img_path)) + 's')
        print("age: " + str(fiAgeMinutes(img_path)) + 'min')
        print("age: " + str(fiAgeHours(img_path)) + 'h')
        
        print('\nrm 1.png')
        fiRemove(os.path.join(d, "sub_dir", "1.png"))
        print("files:\n" + "\n".join(fiFindByWildcard(os.path.join(d, "**", "*"))))
        
        if fiIsEmptyDir(out_dir):
            print("\nRemove empty dir")
            fiRemoveDir(out_dir)
        print("files: " + "\n".join(fiFindByWildcard(os.path.join(d, "**", "*"))))


# # Jupyter

# In[172]:


def jnNbFullWidth():
    from IPython.core.display import display, HTML
    display(HTML("<style>.container { width:100% !important; }</style>"))
    
def jnPandasSettings():
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', None)


# In[173]:


def jnImageRenderingPixelated():
    """Do not interpolate images"""
    display(HTML('<style type = text/css> img { image-rendering: pixelated; } </style>'))
    
def jnImageRenderingAuto():
    """Interpolate images"""
    display(HTML('<style type = text/css> img { image-rendering: auto; } </style>'))


# In[174]:


def jnDefault():
    jnNbFullWidth()
    jnPandasSettings()
    jnImageRenderingPixelated

if is_testing():
    jnDefault()


# In[175]:


def jnHtmlRow(strList, width=100):
    to_col = lambda x: '<td style="text-align:center">' + x + '</td>'
    display(HTML('<table width="{width}%"><tr>{cols}</tr></table>'.format(width=width, cols="".join(map(to_col, strList)))))

if is_testing():
    jnHtmlRow(['text', 'looooooooooooong text', 'text'])
    jnHtmlRow(['text', 'looooooooooooong text', 'text'], width=50)
    


# In[176]:


def jnImgToHtmlB64(img):
    img = imread(img)
    _, encimg = cv2.imencode('.png', img[:, :, [2, 1, 0]])
    imgB64 = base64.b64encode(encimg).decode('utf-8')
    img_tag = '<img src="data:image/png;base64,{0}" style="display:block; margin:0 auto;">'.format(imgB64)
    return img_tag

#def jnHtmlImgsRow(imgs, names=None):

def jnImageRow(imgs, names=None, width=100, external=False, title_img=None, title=None):
    if isinstance(imgs, OrderedDict):
        names, imgs = list(zip(*imgs.items()))
        
    _row = lambda x: '<tr>' + x + '</tr>'
    _col = lambda x: '<td style="text-align:center; word-wrap:break-word;">' + x + '</td>'
    _nacols = lambda x: prefix_name + "".join(map(_col, x))
    
    prefix_name = "" if title is None else _col(title)
    prefix_img = "" if title is None else _col("")

    if external:
        _imcols = lambda x: prefix_img + "".join(map(_col, map(lambda y: '<img src="{}" style="display:block; margin:0 auto;">'.format(y), x)))
    else:
        _imcols = lambda x: prefix_img + "".join(map(_col, map(jnImgToHtmlB64, x)))
        
    _tab = lambda x: '<table width="{width}%">'.format(width=width) + x + '</table>'
    
    header = "" if names is None else _row(_nacols(names))
    html = _tab(header + _row(_imcols(imgs)))
    display(HTML(html))


# In[177]:


if is_testing():
    jnImageRow(imgs=[imNewBlack(20, 20), imNewBlack(40, 20), imNewBlack(20, 800)], names=["longWordNoSpace"*10, "b", "c"])
   


# In[178]:


if is_testing():
    imgs = OrderedDict()
    imgs['a'] = "http://via.placeholder.com/40x20.png"
    imgs['b'] = "http://via.placeholder.com/40x20.png"
    jnImageRow(imgs, external=True, title='test')


# In[179]:



if is_testing():
   jnImageRow(imgs=[imNewBlack(20, 20), imNewBlack(40, 20), imNewBlack(20, 800)])


# # Shell

# In[180]:


def shell(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    out = result.stdout.decode()
    
    if len(out) > 0 and out[-1] == "\n":
        out = out[:-1]
        
    return out


# # GIT

# In[181]:


def gitGetHash():
    return shell('git rev-parse HEAD').strip()

if is_testing():
    print(gitGetHash())


# In[182]:


def gitGetBranch():
    return shell('git rev-parse --abbrev-ref HEAD').strip()

if is_testing():
    print(gitGetBranch())


# In[183]:


def gitGetMessage():
    return shell('git log --format=%B -n 1 HEAD').strip()

if is_testing():
    print(gitGetMessage())


# In[184]:


def gitGetAllFiles():
    return shell('git ls-tree -r --name-only HEAD').split("\n")

if is_testing():
    print(gitGetAllFiles())


# In[185]:


def gitListByTime(path=None):
    cd = '' if path is None else 'cd ' + path + ' &&'
    
    _time = lambda x: shell(cd + 'git log -1 --format="%ad" --date=raw -- {filename}'.format(filename=x))
    paths = shell(cd + 'git ls-tree -r --name-only HEAD').split("\n")
    times = list(map(_time, paths))
    
    return [path for _, path in sorted(zip(times, paths))]
    
if is_testing():
    print(gitListByTime()[-3:])


# In[186]:


def shellSortDirsBySize():
    return shell('du -h | sort -h')

if is_testing():
    print(shellSortDirsBySize())


# # Package Files

# In[187]:


if is_testing():
    package_files = {}


# In[188]:


def shell(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode()


# In[189]:


if is_testing():
    package_files['setup.py'] = r"""from distutils.core import setup
setup(
  name = 'lx',         # How you named your package folder (MyLib)
  packages = ['lx'],   # Chose the same as "name"
  version = '{version}',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'lx',   # Give a short description about your library
  author = 'lx',                   # Type in your name
  author_email = 'hx2983113@gmail.com',      # Type in your E-Mail
  #url = 'https://github.com/hx2983113/lx',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/hx2983113/lx/archive/0.20.tar.gz',    # I explain this later on
  keywords = [],   # Keywords that define your package best
  install_requires=[
      {requirements}
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)""".format(requirements=", ".join(["'" + r + "'" for r in requirements]), version=version)


# In[190]:


if is_testing():
    package_files['setup.cfg'] = r"""# Inside of setup.cfg
[metadata]
description-file = README.md
"""


# In[191]:


if is_testing():
    package_files['LICENSE.txt'] = r"""MIT License
Copyright (c) 2018 YOUR NAME
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


# In[192]:


if is_testing():
    package_files['README.md'] = ""


# In[193]:


if is_testing():
    shell("jupyter nbconvert --to script lx.ipynb")
    package_files['lx/__init__.py'] = txtread("lx.py")
    


# In[194]:


if is_testing():
    package_files['MANIFEST'] = r"""# file GENERATED by distutils, do NOT edit
setup.cfg
setup.py
lx/__init__.py
"""


# In[195]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        for key, value in package_files.items():
            txtwrite(os.path.join(d, key), value)

        print("\n".join(fiFindByWildcard(os.path.join(d, '**/*'))))
        
        output = shell("""python3 -c 'import importlib; lx = importlib.import_module(name=".", package="lx"); print(lx.version)'""")
        print(output.strip(), 'Version correct: ', output.strip() == version)
        
        if output.strip() == version:
            #print(shell("cd {d} && git status && git config user.name 'lx' && git config user.email 'lx' && git commit -a -m 'Add' && git log && git push && python setup.py sdist && twine upload dist/* --verbose".format(d=d)))
            print(shell("cd {d} && python3 setup.py sdist && twine upload dist/* --verbose".format(d=d)))

